from fastapi import APIRouter, Depends
from pymongo.asynchronous.database import AsyncDatabase

from backend.database.mongodb import get_database

router = APIRouter(prefix="/api/geofences", tags=["geofences"])


@router.get("")
async def list_active_geofences(db: AsyncDatabase = Depends(get_database)):
    zones = await db["geofence_zones"].find({"is_active": True, "zone_type": "circle"}).to_list(length=None)
    return [{"id": str(zone["_id"]), "poi_id": str(zone["poi_id"]), "radius": zone["radius"], "geometry": zone["geometry"]} for zone in zones]
