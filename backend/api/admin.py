from datetime import datetime, timedelta, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from pymongo.asynchronous.database import AsyncDatabase

from backend.database.mongodb import get_database
from backend.services.admin_auth import require_permission
from backend.api.audio import get_audio_storage_provider
from backend.services.audio_storage import AudioStorageProvider

router = APIRouter(prefix="/api/admin", tags=["admin"])
LANGUAGES = {"vi", "en", "zh-Hans", "ja", "ko", "fr"}


class PoiInput(BaseModel):
    name: str = Field(min_length=1, max_length=180)
    category: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=3000)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    image_url: str = ""
    is_active: bool = True


class LocalizationInput(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    description: str = Field(min_length=1, max_length=10000)
    tts_status: str = "draft"


@router.get("/geofences")
async def list_geofences(_=Depends(require_permission("poi:write")), db: AsyncDatabase = Depends(get_database)):
    zones = await db["geofence_zones"].find({}).sort("created_at", -1).to_list(length=None)
    return [{"id": str(zone["_id"]), "poi_id": str(zone["poi_id"]), "zone_type": zone.get("zone_type"), "radius": zone.get("radius"), "is_active": zone.get("is_active", False)} for zone in zones]


@router.get("/pois")
async def list_pois(language: str = Query("vi"), _=Depends(require_permission("poi:write")), db: AsyncDatabase = Depends(get_database)):
    if language not in LANGUAGES:
        raise HTTPException(status_code=422, detail="Unsupported language")
    pois = await db["poi"].find({}).sort("name", 1).to_list(length=None)
    localizations = await db["poi_localizations"].find({"poi_id": {"$in": [poi["_id"] for poi in pois]}, "language_code": language}).to_list(length=None)
    localized = {item["poi_id"]: item for item in localizations}
    return [{
        "id": str(poi["_id"]), "name": poi.get("name", ""), "category": poi.get("category", ""),
        "system_description": poi.get("description", ""),
        "description": localized.get(poi["_id"], {}).get("description", poi.get("description", "")),
        "title": localized.get(poi["_id"], {}).get("title", poi.get("name", "")),
        "latitude": poi.get("latitude"), "longitude": poi.get("longitude"),
        "image_url": poi.get("image_url", ""), "is_active": poi.get("is_active", False),
        "has_localization": poi["_id"] in localized,
        "audio_url": localized.get(poi["_id"], {}).get("audio_url"),
        "tts_status": localized.get(poi["_id"], {}).get("tts_status", "draft"),
    } for poi in pois]


@router.post("/pois", status_code=201)
async def create_poi(data: PoiInput, _=Depends(require_permission("poi:write")), db: AsyncDatabase = Depends(get_database)):
    now = datetime.now(timezone.utc)
    doc = data.model_dump() | {"created_at": now, "updated_at": now,
        "geometry": {"type": "Point", "coordinates": [data.longitude, data.latitude]}}
    result = await db["poi"].insert_one(doc)
    return {"id": str(result.inserted_id)}


@router.put("/pois/{poi_id}")
async def update_poi(poi_id: str, data: PoiInput, _=Depends(require_permission("poi:write")), db: AsyncDatabase = Depends(get_database)):
    if not ObjectId.is_valid(poi_id):
        raise HTTPException(status_code=400, detail="Invalid POI ID")
    values = data.model_dump() | {"updated_at": datetime.now(timezone.utc), "geometry": {"type": "Point", "coordinates": [data.longitude, data.latitude]}}
    result = await db["poi"].update_one({"_id": ObjectId(poi_id)}, {"$set": values})
    if not result.matched_count:
        raise HTTPException(status_code=404, detail="POI not found")
    await db["geofence_zones"].update_many({"poi_id": ObjectId(poi_id), "zone_type": "circle"}, {"$set": {"geometry": values["geometry"]}})
    return {"updated": True}


@router.delete("/pois/{poi_id}")
async def deactivate_poi(poi_id: str, _=Depends(require_permission("poi:write")), db: AsyncDatabase = Depends(get_database)):
    if not ObjectId.is_valid(poi_id):
        raise HTTPException(status_code=400, detail="Invalid POI ID")
    result = await db["poi"].update_one({"_id": ObjectId(poi_id)}, {"$set": {"is_active": False, "updated_at": datetime.now(timezone.utc)}})
    if not result.matched_count:
        raise HTTPException(status_code=404, detail="POI not found")
    return {"deactivated": True}


@router.put("/pois/{poi_id}/localizations/{language}")
async def save_localization(poi_id: str, language: str, data: LocalizationInput, _=Depends(require_permission("content:write")), db: AsyncDatabase = Depends(get_database)):
    if not ObjectId.is_valid(poi_id):
        raise HTTPException(status_code=400, detail="Invalid POI ID")
    if language not in LANGUAGES:
        raise HTTPException(status_code=422, detail="Unsupported language")
    oid = ObjectId(poi_id)
    if not await db["poi"].find_one({"_id": oid}):
        raise HTTPException(status_code=404, detail="POI not found")
    previous = await db["poi_localizations"].find_one({"poi_id": oid, "language_code": language})
    values = data.model_dump() | {"updated_at": datetime.now(timezone.utc)}
    changed = previous is None or any(previous.get(key) != values[key] for key in ("title", "description"))
    if changed:
        values.update({"audio_url": None, "tts_status": "draft", "audio_status": "STALE_REQUIRES_REGENERATION"})
    await db["poi_localizations"].update_one(
        {"poi_id": oid, "language_code": language},
        {"$set": values, "$setOnInsert": {"poi_id": oid, "language_code": language}},
        upsert=True,
    )
    return {"saved": True, "content_status": "draft"}


@router.get("/analytics/summary")
async def analytics_summary(_=Depends(require_permission("analytics:read")), db: AsyncDatabase = Depends(get_database)):
    now = datetime.now(timezone.utc)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    events = db["analytics_events"]
    current_match = {"timestamp": {"$gte": today}}
    active_match = {"timestamp": {"$gte": now - timedelta(minutes=5)}}

    async def aggregate_rows(pipeline: list[dict], limit: int) -> list[dict]:
        cursor = await events.aggregate(pipeline)
        return await cursor.to_list(length=limit)

    import asyncio
    total_events, today_events, total_visits, today_visits, active_devices = await asyncio.gather(
        events.count_documents({}),
        events.count_documents(current_match),
        aggregate_rows([{"$match": {"event_type": "session_start"}}, {"$group": {"_id": "$session_id"}}, {"$count": "count"}], 1),
        aggregate_rows([{"$match": {"event_type": "session_start", **current_match}}, {"$group": {"_id": "$session_id"}}, {"$count": "count"}], 1),
        aggregate_rows([
            {"$match": active_match},
            {"$lookup": {"from": "analytics_sessions", "localField": "session_id", "foreignField": "_id", "as": "session"}},
            {"$unwind": "$session"},
            {"$group": {"_id": "$session.device_id"}},
            {"$count": "count"},
        ], 1),
    )
    event_counts = await aggregate_rows([
        {"$match": current_match},
        {"$group": {"_id": "$event_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ], 20)
    top_pois = await aggregate_rows([
        {"$match": {"timestamp": {"$gte": today}, "poi_id": {"$ne": None}, "event_type": {"$in": ["poi_view", "qr_scan", "playback_start"]}}},
        {"$group": {"_id": "$poi_id", "interactions": {"$sum": 1}}},
        {"$sort": {"interactions": -1}}, {"$limit": 8},
        {"$lookup": {"from": "poi", "localField": "_id", "foreignField": "_id", "as": "poi"}},
        {"$unwind": {"path": "$poi", "preserveNullAndEmptyArrays": True}},
        {"$project": {"_id": 0, "poi_id": {"$toString": "$_id"}, "name": {"$ifNull": ["$poi.name", "Điểm tham quan"]}, "interactions": 1}},
    ], 8)
    languages = await aggregate_rows([
        {"$match": {"timestamp": {"$gte": today}, "event_type": {"$in": ["page_view", "qr_scan", "playback_start", "playback_complete"]}}},
        {"$group": {"_id": {"$ifNull": ["$data.language_code", "unknown"]}, "visits": {"$sum": 1}}},
        {"$sort": {"visits": -1}},
    ], 10)
    daily = await aggregate_rows([
        {"$match": {"timestamp": {"$gte": today - timedelta(days=6)}, "event_type": "session_start"}},
        {"$group": {"_id": {"day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp", "timezone": "UTC"}}, "session": "$session_id"}}},
        {"$group": {"_id": "$_id.day", "visits": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ], 7)
    hourly = await aggregate_rows([
        {"$match": {"timestamp": {"$gte": today}, "event_type": "session_start"}},
        {"$group": {"_id": {"hour": {"$hour": {"date": "$timestamp", "timezone": "UTC"}}, "session": "$session_id"}}},
        {"$group": {"_id": "$_id.hour", "visits": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ], 24)
    playback_starts = next((row["count"] for row in event_counts if row["_id"] == "playback_start"), 0)
    playback_completes = next((row["count"] for row in event_counts if row["_id"] == "playback_complete"), 0)
    return {
        "generated_at": now.isoformat(), "active_devices": active_devices[0]["count"] if active_devices else 0,
        "visits_today": today_visits[0]["count"] if today_visits else 0, "visits_total": total_visits[0]["count"] if total_visits else 0, "events_today": today_events, "total_events": total_events,
        "audio_starts_today": playback_starts, "audio_completions_today": playback_completes,
        "audio_completion_rate_today": round(playback_completes / playback_starts * 100, 1) if playback_starts else 0,
        "event_counts": [{"event_type": row["_id"], "count": row["count"]} for row in event_counts],
        "top_pois": top_pois, "languages_today": [{"language": row["_id"] or "unknown", "visits": row["visits"]} for row in languages],
        "daily_visits": [{"date": row["_id"], "visits": row["visits"]} for row in daily],
        "hourly_visits": [{"hour": row["_id"], "visits": row["visits"]} for row in hourly],
    }


@router.get("/audio-assets")
async def list_audio_assets(language: str = Query("vi"), _=Depends(require_permission("audio:write")), db: AsyncDatabase = Depends(get_database), storage: AudioStorageProvider = Depends(get_audio_storage_provider)):
    assets = await db["audio_assets"].find({"language_code": language}).sort("created_at", -1).to_list(length=500)
    rows = []
    for asset in assets:
        info = await storage.inspect(asset["file_url"])
        rows.append({"id": str(asset["_id"]), "poi_id": str(asset["poi_id"]), "language_code": asset["language_code"], "duration": asset.get("duration", 0), "file_size": info.size if info else None, "checksum": asset.get("checksum", ""), "package_id": str(asset["package_id"]) if asset.get("package_id") else None})
    return rows
