import datetime
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import BigInteger, Field, Session, SQLModel, create_engine, select, true


class Users(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str
    osu_access_token: str
    osu_refresh_token: str
    osu_token_expires_at: datetime.datetime
    app_refresh_token: str
    app_token_expires_at: datetime.datetime
