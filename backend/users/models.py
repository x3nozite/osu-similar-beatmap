import datetime
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import BigInteger, Field, Session, SQLModel, create_engine, select, true


class Users(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str
    access_token: str
    refresh_token: str
    token_expires_at: datetime.datetime
