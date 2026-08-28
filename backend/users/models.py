import datetime
from sqlmodel import TIMESTAMP, BigInteger, Column, DateTime, Field, Session, SQLModel, String, create_engine, select, true


class Users(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str
    osu_access_token: str = Field(sa_column=Column("access_token", String))
    osu_refresh_token: str = Field(sa_column=Column("refresh_token", String))
    osu_token_expires_at: datetime.datetime = Field(
        sa_column=Column("token_expires_at", DateTime))
    app_refresh_token: str
    app_token_expires_at: datetime.datetime
