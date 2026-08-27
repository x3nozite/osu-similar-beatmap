from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlmodel import Session, create_engine, select, or_
from urllib.parse import urlencode
from beatmaps.models import Beatmaps
from users.models import Users
import os
from dotenv import load_dotenv
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

postgres_name = "beatmap_similarity"
postgres_url = f"postgresql://postgres:@localhost:5432/{postgres_name}"
engine = create_engine(postgres_url)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

load_dotenv()
osu_secret = os.getenv("OSU_CLIENT_SECRET")


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/test/", response_class=HTMLResponse)
async def test():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


@app.get("/api/search")
def search_beatmapset(q: str, session: SessionDep,) -> list[Beatmaps]:
    if q == '':
        beatmaps = session.exec(
            select(Beatmaps).order_by(Beatmaps.beatmap_id.desc()).limit(50)
        )
        return list(beatmaps)

    tokens = q.split()
    conditions = []
    for t in tokens:
        conditions.append(
            or_(
                Beatmaps.title.ilike(f"%{t}%"),
                Beatmaps.artist.ilike(f"%{t}%"),
                Beatmaps.mapper.ilike(f"%{t}%"),
                Beatmaps.version.ilike(f"%{t}%"),
            )
        )

    beatmaps = session.exec(
        select(Beatmaps).where(*conditions).limit(20)).all()
    return list(beatmaps)


@app.get("/api/beatmap/random")
def random_beatmap(session: SessionDep) -> Beatmaps:
    beatmap = session.exec(
        select(Beatmaps).order_by(func.random())
    ).first()
    if beatmap is None:
        raise HTTPException(status_code=404, detail="No beatmaps found")
    return beatmap


@app.get("/api/search/beatmapsets/{beatmapset_id}")
async def read_beatmapset(beatmapset_id):
    return {"id": beatmapset_id}


@app.post("/api/login")
def osu_login():
    base_url = "https://osu.ppy.sh/oauth/authorize"
    params = {
        'client_id': '66324',
        'redirect_uri': 'http://localhost:8000/api/login/callback',
        'response_type': 'code',
        'scope': 'public identity',
        "state": "randomval",
    }

    url = f"{base_url}?{urlencode(params)}"
    return RedirectResponse(url)


@app.post("api/login/callback")
async def callback(code: str, session: SessionDep):
    if not code:
        raise HTTPException(
            status_code=400, detail="Missing authorization code")

    token_url = "https://osu.ppy.sh/oauth/token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    body = {
        'client_id': '66324',
        'client_secret': osu_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/api/login/callback'
    }

    response = requests.post(token_url, headers=headers, data=body)
    token_data = response.json()

    if response.status_code != 200:
        return {"message": "Failed to get token data"}

    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]
    expires_in = token_data["expires_in"]

    user_url = "https://osu.ppy.sh/api/v2/me"
    user_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    user_info_response = requests.get(user_url, headers=user_headers)
    user_info = user_info_response.json()

    user = session.exec(
        select(Users).where(Users.user_id == user_info["id"])
    ).first()

    if user is not None:
        user.access_token = access_token
        user.refresh_token = refresh_token
        user.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
        session.add(user)
        session.commit()
    else:
        user = Users(
            username=user_info["username"],
            user_id=user_info["id"],
            access_token=access_token,
            refresh_token=refresh_token,
            token_expires_at=datetime.now() + timedelta(seconds=expires_in)
        )
        session.add(user)
        session.commit()

    # setup jwt
