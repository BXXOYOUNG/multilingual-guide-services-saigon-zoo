import hashlib
import hmac
import secrets
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis

from backend.database.mongodb import get_database
from backend.database.redis_client import get_redis_client

SESSION_COOKIE = "tcv_admin_session"
SESSION_TTL_SECONDS = 8 * 60 * 60


def hash_password(password: str, salt: bytes | None = None) -> str:
    if len(password) < 12:
        raise ValueError("Password must contain at least 12 characters")
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, salt_hex, expected = stored.split("$", 2)
        if algorithm != "scrypt":
            return False
        actual = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def _cookie_secure() -> bool:
    return __import__("os").getenv("ADMIN_COOKIE_SECURE", "false").lower() == "true"


async def login_admin(username: str, password: str, response: Any) -> dict[str, str]:
    redis: Redis = get_redis_client()
    login_key = "admin-login-limit:" + hashlib.sha256(username.strip().lower().encode()).hexdigest()
    attempts = await redis.incr(login_key)
    if attempts == 1:
        await redis.expire(login_key, 60)
    if attempts > 10:
        raise HTTPException(status_code=429, detail="Quá nhiều lần đăng nhập. Thử lại sau một phút.")
    database = get_database()
    user = await database["admin_users"].find_one({"username": username})
    if not user or not user.get("is_active") or not verify_password(password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng")

    role = await database["roles"].find_one({"_id": user.get("role_id")})
    if not role:
        raise HTTPException(status_code=403, detail="Tài khoản chưa được gán vai trò")

    token = secrets.token_urlsafe(32)
    await redis.setex(f"admin-session:{token}", SESSION_TTL_SECONDS, str(user["_id"]))
    await redis.delete(login_key)
    response.set_cookie(
        SESSION_COOKIE, token, max_age=SESSION_TTL_SECONDS, httponly=True,
        secure=_cookie_secure(), samesite="lax", path="/",
    )
    await database["admin_users"].update_one({"_id": user["_id"]}, {"$set": {"last_login": __import__("datetime").datetime.now(__import__("datetime").timezone.utc)}})
    return {"username": user["username"], "role": role.get("name", "")}


async def require_admin(request: Request) -> dict[str, Any]:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cần đăng nhập quản trị")
    redis: Redis = get_redis_client()
    user_id = await redis.get(f"admin-session:{token}")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Phiên quản trị đã hết hạn")
    from bson import ObjectId
    database = get_database()
    user = await database["admin_users"].find_one({"_id": ObjectId(user_id), "is_active": True})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tài khoản quản trị không còn hoạt động")
    role = await database["roles"].find_one({"_id": user.get("role_id")})
    user["permissions"] = role.get("permissions", []) if role else []
    return user


def require_permission(permission: str):
    async def dependency(user: dict[str, Any] = Depends(require_admin)) -> dict[str, Any]:
        if permission not in user.get("permissions", []):
            raise HTTPException(status_code=403, detail="Không đủ quyền thực hiện thao tác")
        return user

    return dependency
