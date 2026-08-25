from operator import and_
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import session
from sqlalchemy import func
from sqlmodel import Session, create_engine, select

from beatmaps.models import Beatmaps

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
    conditions = [Beatmaps.title.ilike(f"%{t}%") for t in tokens]

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
