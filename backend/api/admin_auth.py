import os

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, Field
from backend.database.mongodb import get_database
from backend.database.redis_client import get_redis_client
from backend.services.admin_auth import (
    SESSION_COOKIE, SESSION_TTL_SECONDS, login_admin, require_admin,
    hash_password, verify_password,
)

router = APIRouter(prefix="/api/admin/auth", tags=["admin-auth"])


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1, max_length=256)


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=256)
    new_password: str = Field(min_length=12, max_length=256)


@router.post("/login")
async def login(request: LoginRequest, response: Response):
    return await login_admin(request.username, request.password, response)


@router.get("/session")
async def session(user=Depends(require_admin)):
    return {"username": user["username"], "permissions": user.get("permissions", [])}


@router.post("/logout")
async def logout(request: Request, response: Response, user=Depends(require_admin)):
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        await get_redis_client().delete(f"admin-session:{token}")
    response.delete_cookie(SESSION_COOKIE, path="/", httponly=True, secure=os.getenv("ADMIN_COOKIE_SECURE", "false").lower() == "true", samesite="lax")
    return {"ok": True}


@router.post("/password")
async def change_password(request: PasswordChangeRequest, user=Depends(require_admin)):
    database = get_database()
    stored = user.get("password_hash", "")
    if not verify_password(request.current_password, stored):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Mật khẩu hiện tại không đúng")
    await database["admin_users"].update_one(
        {"_id": user["_id"]},
        {"$set": {"password_hash": hash_password(request.new_password)}},
    )
    return {"updated": True}
