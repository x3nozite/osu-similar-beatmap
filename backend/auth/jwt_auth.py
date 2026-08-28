from datetime import datetime, timedelta, timezone
from typing import Annotated
import secrets

from fastapi import Depends, HTTPException, Request
import jwt
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlmodel import select

from database import SessionDep
from users.models import Users

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow(
    ) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)


def revoke_tokens():
    # remove from cookies + db
    pass


def get_current_user(request: Request, session: SessionDep):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    osu_user_id = payload.get("osu_user_id")
    if osu_user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = session.exec(select(Users).where(
        Users.user_id == osu_user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
