"""Create the first admin using the existing roles/admin_users ERD collections."""
import asyncio
import getpass
import os
from datetime import datetime, timezone

from pymongo import AsyncMongoClient

from backend.services.admin_auth import hash_password


async def main():
    uri = os.environ.get("MONGODB_URI")
    database_name = os.environ.get("MONGODB_DATABASE")
    if not uri or not database_name:
        raise SystemExit("Set MONGODB_URI and MONGODB_DATABASE before running this command.")
    username = input("Admin username: ").strip()
    email = input("Admin email: ").strip()
    password = getpass.getpass("Admin password (12+ characters): ")
    if not username or not email:
        raise SystemExit("Username and email are required.")
    try:
        password_hash = hash_password(password)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    client = AsyncMongoClient(uri)
    try:
        db = client[database_name]
        existing = await db["admin_users"].find_one({"$or": [{"username": username}, {"email": email}]})
        if existing:
            raise SystemExit("An admin already uses this username or email.")
        now = datetime.now(timezone.utc)
        role = await db["roles"].find_one({"name": "administrator"})
        permissions = ["poi:write", "content:write", "audio:write", "analytics:read"]
        if role is None:
            result = await db["roles"].insert_one({
                "name": "administrator",
                "description": "Full access to the zoo guide admin area",
                "permissions": permissions,
                "created_at": now,
                "updated_at": now,
            })
            role_id = result.inserted_id
        else:
            role_id = role["_id"]
            await db["roles"].update_one({"_id": role_id}, {"$set": {"permissions": permissions, "updated_at": now}})
        await db["admin_users"].insert_one({
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "role_id": role_id,
            "is_active": True,
            "last_login": None,
            "created_at": now,
        })
        print("Admin account created.")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
