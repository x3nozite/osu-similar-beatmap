from datetime import datetime, timedelta, timezone
from typing import Annotated
import secrets

from fastapi import Depends, HTTPException, Request, status, APIRouter
from fastapi.responses import JSONResponse
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


router = APIRouter()


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


@router.get("/api/me")
def me(user: Users = Depends(get_current_user)):
    return {
        "username": user.username,
        "osu_id": user.user_id
    }


@router.post("/api/token/refresh")
def refresh(request: Request, session: SessionDep):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    user = session.exec(select(Users).where(
        Users.app_refresh_token == refresh_token)).first()
    if user is None or user.app_token_expires_at < datetime.now():
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    new_access_token = create_access_token({
        "osu_user_id": user.user_id,
        "username": user.username
    })
    response = JSONResponse({"message": "refreshed"})
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return response
