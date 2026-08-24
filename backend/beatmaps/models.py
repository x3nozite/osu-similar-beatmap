from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import BigInteger, Field, Session, SQLModel, create_engine, select, true


class Beatmaps(SQLModel, table=True):
    beatmap_id: int = Field(default=None, primary_key=True)
    beatmapset_id: int
    title: str = Field(default=None)
    star_rating: float
