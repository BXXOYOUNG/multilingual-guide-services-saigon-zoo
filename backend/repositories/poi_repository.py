from typing import Any

from pymongo.asynchronous.database import AsyncDatabase

from backend.schemas.poi import POIResponse


class POIRepository:
    def __init__(self, database: AsyncDatabase) -> None:
        self._database = database

    async def list_for_language(self, language: str) -> list[POIResponse]:
        poi_cursor = self._database["poi"].find(
            {"is_active": True},
            {"_id": 1, "latitude": 1, "longitude": 1},
        )
        pois = [poi async for poi in poi_cursor]
        if not pois:
            return []

        localizations_cursor = self._database["poi_localizations"].find(
            {
                "poi_id": {"$in": [poi["_id"] for poi in pois]},
                "language_code": language,
            },
            {
                "_id": 0,
                "poi_id": 1,
                "title": 1,
                "description": 1,
            },
        )
        localizations: dict[Any, dict[str, Any]] = {
            localization["poi_id"]: localization
            async for localization in localizations_cursor
        }

        return [
            POIResponse(
                id=str(poi["_id"]),
                name=localizations[poi["_id"]]["title"],
                description=localizations[poi["_id"]]["description"],
                latitude=poi["latitude"],
                longitude=poi["longitude"],
            )
            for poi in pois
            if poi["_id"] in localizations
        ]
