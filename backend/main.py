from datetime import timedelta, datetime

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlmodel import Session, create_engine, select, or_
from urllib.parse import urlencode
from auth import jwt_auth
from auth.jwt_auth import router as jwt_router
from beatmaps.models import Beatmaps
from database import SessionDep
from lifespan import lifespan
from users.models import Users
import os
from dotenv import load_dotenv
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

load_dotenv()
osu_secret = os.getenv("OSU_CLIENT_SECRET")


app.include_router(jwt_router)


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
def search_beatmapset(q: str, session: SessionDep) -> list[Beatmaps]:
    if q == '':
        beatmaps = session.exec(
            select(Beatmaps).order_by(Beatmaps.beatmapset_id.desc()).limit(50)
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

    beatmapset_ids = session.exec(
        select(Beatmaps.beatmapset_id).where(*conditions).distinct().limit(50)
    ).all()

    beatmaps = session.exec(
        select(Beatmaps).where(Beatmaps.beatmapset_id.in_(beatmapset_ids)).order_by(Beatmaps.star_rating.asc())).all()
    return list(beatmaps)


@app.get("/api/beatmap/random")
def random_beatmap(session: SessionDep) -> Beatmaps:
    beatmap = session.exec(
        select(Beatmaps).order_by(func.random())
    ).first()
    if beatmap is None:
        raise HTTPException(status_code=404, detail="No beatmaps found")
    return beatmap


@app.get("/api/beatmap/{beatmap_id}")
def get_beatmap(beatmap_id, session: SessionDep) -> Beatmaps:
    beatmap = session.exec(
        select(Beatmaps).where(Beatmaps.beatmap_id == beatmap_id)
    ).first()
    if beatmap is None:
        raise HTTPException(status_code=404, detail="No beatmaps found")
    return beatmap


@app.get("/api/search/beatmapsets/{beatmapset_id}")
async def read_beatmapset(beatmapset_id):
    return {"id": beatmapset_id}


@app.get("/api/login")
def osu_login():
    base_url = "https://osu.ppy.sh/oauth/authorize"
    params = {
        'client_id': '66324',
        'redirect_uri': 'http://localhost:8000/api/login/callback',
        'response_type': 'code',
        'scope': 'public identify',
        "state": "randomval",
    }

    url = f"{base_url}?{urlencode(params)}"
    return RedirectResponse(url)


@app.get("/api/login/callback")
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
    print("test")

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

    app_access_token = jwt_auth.create_access_token({
        "osu_user_id": user_info["id"],
        "username": user_info["username"]
    })
    app_refresh_token = jwt_auth.create_refresh_token()

    if user is not None:
        user.osu_access_token = access_token
        user.osu_refresh_token = refresh_token
        user.osu_token_expires_at = datetime.now() + timedelta(seconds=expires_in)
        user.app_refresh_token = app_refresh_token
        user.app_token_expires_at = datetime.now() + timedelta(days=365)
        session.add(user)
        session.commit()
    else:
        user = Users(
            username=user_info["username"],
            user_id=user_info["id"],
            osu_access_token=access_token,
            osu_refresh_token=refresh_token,
            osu_token_expires_at=datetime.now() + timedelta(seconds=expires_in),
            app_refresh_token=app_refresh_token,
            app_token_expires_at=datetime.now() + timedelta(days=365)
        )
        session.add(user)
        session.commit()

    # TODO: change with actual deployment url later
    response = RedirectResponse(url="http://localhost:3000/")

    response.set_cookie(
        key="access_token",
        value=app_access_token,
        httponly=True,
        secure=False,  # TODO: change to True for production/HTTPS
        samesite="lax",
        max_age=jwt_auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    response.set_cookie(
        key="refresh_token",
        value=app_refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=365 * 24 * 60 * 60
    )

    return response


# TODO: filter same beatmapset_id from being picked as a similar beatmap
@app.get("/api/beatmap/{beatmap_id}/similar")
def get_similar(beatmap_id: int, request: Request, session: SessionDep, limit: int = 20):
    numeric_m = request.app.state.numeric_matrix
    beatmap_id_idx = request.app.state.beatmap_id_index
    tag_m = request.app.state.tag_matrix
    beatmapset_id_idx = request.app.state.beatmapset_id_index
    beatmap_to_beatmapset = request.app.state.beatmap_to_beatmapset

    if beatmap_id not in beatmap_id_idx:
        raise HTTPException(status_code=404, detail="Beatmap not found")

    target_row = beatmap_id_idx[beatmap_id]
    target_vector = numeric_m[target_row]

    numeric_dist = np.linalg.norm(numeric_m - target_vector, axis=1)
    numeric_similarity = 1 / (1 + numeric_dist)

    target_beatmap = session.get(Beatmaps, beatmap_id)
    if not target_beatmap:
        raise HTTPException(status_code=404, detail="Beatmap not found")

    tag_similarity = np.zeros(len(numeric_similarity))

    if target_beatmap.beatmapset_id in beatmapset_id_idx:
        row_idx = beatmapset_id_idx[target_beatmap.beatmapset_id]
        tag_sims = cosine_similarity(tag_m[row_idx], tag_m).flatten()

        for bm_id_, idx in beatmap_id_idx.items():
            bms_id = beatmap_to_beatmapset[bm_id_]
            if bms_id in beatmapset_id_idx:
                tag_similarity[idx] = tag_sims[beatmapset_id_idx[bms_id]]

    similarity_score = 0.6 * numeric_similarity + 0.4 * tag_similarity

    similarity_score[target_row] = -1
    top_scorers = np.argsort(similarity_score)[::-1][:limit]

    idx_to_beatmap_id = {idx: bm_id for bm_id, idx in beatmap_id_idx.items()}
    top_ids = [idx_to_beatmap_id[i] for i in top_scorers]

    similar_beatmaps = session.exec(
        select(Beatmaps).where(Beatmaps.beatmap_id.in_(top_ids))
    ).all()
    return similar_beatmaps
