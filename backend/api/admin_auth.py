import os
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from backend.database.mongodb import get_database
from backend.database.redis_client import get_redis_client
from backend.services.admin_auth import (
    SESSION_COOKIE, SESSION_TTL_SECONDS, login_admin, require_admin_session,
    hash_password, verify_password, password_status,
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
async def session(user=Depends(require_admin_session)):
    return {"username": user["username"], "permissions": user.get("permissions", []), **password_status(user)}


@router.post("/logout")
async def logout(request: Request, response: Response, user=Depends(require_admin_session)):
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        await get_redis_client().delete(f"admin-session:{token}")
    response.delete_cookie(SESSION_COOKIE, path="/", httponly=True, secure=os.getenv("ADMIN_COOKIE_SECURE", "false").lower() == "true", samesite="lax")
    return {"ok": True}


@router.post("/password")
async def change_password(request: PasswordChangeRequest, user=Depends(require_admin_session)):
    database = get_database()
    stored = user.get("password_hash", "")
    if not verify_password(request.current_password, stored):
        raise HTTPException(status_code=400, detail="Mật khẩu hiện tại không đúng")
    if verify_password(request.new_password, stored):
        raise HTTPException(status_code=400, detail="Mật khẩu mới phải khác mật khẩu hiện tại")
    changed_at = datetime.now(timezone.utc)
    result = await database["admin_users"].update_one(
        {"_id": user["_id"], "password_hash": stored},
        {"$set": {"password_hash": hash_password(request.new_password), "password_changed_at": changed_at}},
    )
    if not result.matched_count:
        raise HTTPException(status_code=409, detail="Mật khẩu đã thay đổi ở phiên khác. Vui lòng nhập lại mật khẩu hiện tại.")
    return {"updated": True, **password_status({"password_changed_at": changed_at})}