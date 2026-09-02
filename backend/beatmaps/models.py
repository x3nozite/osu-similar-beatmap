from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import BigInteger, Field, Session, SQLModel, create_engine, select, true


class Beatmaps(SQLModel, table=True):
    beatmap_id: int = Field(default=None, primary_key=True)
    beatmapset_id: int = Field(default=None)
    title: str = Field(default=None)
    star_rating: float = Field(default=None)
    version: str = Field(default=None)
    artist: str
    mapper: str
    bpm_norm: float
    diff_aim_norm: float
    diff_speed_norm: float
    ar_norm: float
    cs_norm: float
    density_norm: float
    tap_ratio_norm: float
