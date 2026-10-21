from contextlib import AsyncExitStack, asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from backend.api.audio import router as audio_router
from backend.api.admin_auth import router as admin_auth_router
from backend.api.admin import router as admin_router
from backend.api.health import router as health_router
from backend.api.pois import router as pois_router
from backend.api.visitor import router as visitor_router
from backend.api.geofences import router as geofences_router
from backend.config import load_settings
from backend.core.exception_handlers import register_exception_handlers
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
register_exception_handlers(app)

app.include_router(health_router)
app.include_router(pois_router)
app.include_router(audio_router)
app.include_router(admin_auth_router)
app.include_router(admin_router)
app.include_router(visitor_router)
app.include_router(geofences_router)
