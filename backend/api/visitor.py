from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from pymongo.asynchronous.database import AsyncDatabase

from backend.database.mongodb import get_database
from backend.database.redis_client import get_redis_client

router = APIRouter(prefix="/api", tags=["visitor-events"])


class EventRequest(BaseModel):
    device_id: str
    session_id: str
    visitor_id: str
    event_type: Literal["session_start", "page_view", "heartbeat", "poi_view", "qr_scan", "playback_start", "playback_complete", "geofence_enter", "geofence_exit"]
    poi_id: str | None = None
    language_code: str | None = Field(default=None, max_length=12)
    audio_id: str | None = None
    duration: int | None = Field(default=None, ge=0, le=86400)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


@router.post("/analytics/events", status_code=202)
async def record_event(payload: EventRequest, database: AsyncDatabase = Depends(get_database)):
    if not ObjectId.is_valid(payload.visitor_id):
        raise HTTPException(status_code=400, detail="Invalid visitor_id")
    redis = get_redis_client()
    rate_key = f"visitor-event-limit:{payload.visitor_id}"
    event_count = await redis.incr(rate_key)
    if event_count == 1:
        await redis.expire(rate_key, 60)
    if event_count > 120:
        raise HTTPException(status_code=429, detail="Too many analytics events")
    for name in ("device_id", "session_id"):
        if not ObjectId.is_valid(getattr(payload, name)):
            raise HTTPException(status_code=400, detail=f"Invalid {name}")
    if payload.poi_id and not ObjectId.is_valid(payload.poi_id):
        raise HTTPException(status_code=400, detail="Invalid POI ID")
    if payload.audio_id and not ObjectId.is_valid(payload.audio_id):
        raise HTTPException(status_code=400, detail="Invalid audio ID")

    now = datetime.now(timezone.utc)
    device_id, session_id, visitor_id = map(ObjectId, (payload.device_id, payload.session_id, payload.visitor_id))
    await database["analytics_devices"].update_one(
        {"_id": device_id},
        {"$setOnInsert": {"device_type": "web", "app_version": "web-client", "created_at": now}},
        upsert=True,
    )
    await database["analytics_sessions"].update_one(
        {"_id": session_id},
        {"$setOnInsert": {"device_id": device_id, "user_id": visitor_id, "start_time": now, "end_time": None, "language_code": payload.language_code or "vi"}},
        upsert=True,
    )
    data: dict[str, Any] = {}
    if payload.language_code:
        data["language_code"] = payload.language_code
    if payload.audio_id:
        data["audio_id"] = ObjectId(payload.audio_id)
    if payload.duration is not None:
        data["duration"] = payload.duration
    if payload.latitude is not None and payload.longitude is not None:
        data["latitude"] = payload.latitude
        data["longitude"] = payload.longitude
    event = {
        "session_id": session_id,
        "event_type": payload.event_type,
        "poi_id": ObjectId(payload.poi_id) if payload.poi_id else None,
        "data": data,
        "timestamp": now,
    }
    if payload.event_type == "session_start":
        await database["analytics_events"].update_one(
            {"session_id": session_id, "event_type": "session_start"},
            {"$setOnInsert": event}, upsert=True,
        )
    else:
        await database["analytics_events"].insert_one(event)


    if payload.event_type == "playback_complete" and payload.poi_id and payload.audio_id:
        await database["playback_history"].insert_one({
            "user_id": visitor_id,
            "poi_id": ObjectId(payload.poi_id),
            "language_code": payload.language_code or "vi",
            "audio_id": ObjectId(payload.audio_id),
            "start_time": now - timedelta(seconds=payload.duration or 0),
            "end_time": now,
            "duration": payload.duration or 0,
        })

    if payload.event_type.startswith("geofence_") and payload.latitude is not None and payload.longitude is not None:
        await database["location_events"].insert_one({
            "user_id": visitor_id,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "timestamp": now,
            "accuracy": None,
            "event_type": "Geofence",
        })
    return {"accepted": True}
