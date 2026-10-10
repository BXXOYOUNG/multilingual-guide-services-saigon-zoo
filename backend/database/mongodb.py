from typing import Optional

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from backend.config import MongoSettings

_client: Optional[AsyncMongoClient] = None
_database: Optional[AsyncDatabase] = None


async def connect_mongodb(settings: MongoSettings) -> None:
    global _client, _database

    if _client is not None:
        raise RuntimeError("MongoDB client is already initialized")

    client = AsyncMongoClient(settings.uri)
    try:
        await client.admin.command("ping")
        database = client[settings.database]
    except Exception:
        await client.close()
        raise

    _client = client
    _database = database


def get_database() -> AsyncDatabase:
    if _database is None:
        raise RuntimeError("MongoDB is not configured or has not been initialized")
    return _database


async def close_mongodb() -> None:
    global _client, _database

    client = _client
    _client = None
    _database = None
    if client is not None:
        await client.close()
