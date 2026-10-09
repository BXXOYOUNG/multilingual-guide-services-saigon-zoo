from contextlib import AsyncExitStack, asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from backend.api.health import router as health_router
from backend.config import load_settings
from backend.database.mongodb import close_mongodb, connect_mongodb
from backend.database.redis_client import close_redis, connect_redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = load_settings()
    async with AsyncExitStack() as stack:
        if settings.mongodb is not None:
            await connect_mongodb(settings.mongodb)
            stack.push_async_callback(close_mongodb)
        if settings.redis is not None:
            await connect_redis(settings.redis)
            stack.push_async_callback(close_redis)
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
