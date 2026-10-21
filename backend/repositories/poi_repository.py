from typing import Any

from pymongo.asynchronous.database import AsyncDatabase

from backend.schemas.poi import AnimalCatalogResponse, POIResponse


class POIRepository:
    def __init__(self, database: AsyncDatabase) -> None:
        self._database = database

    async def list_for_language(self, language: str) -> list[POIResponse]:
        poi_cursor = self._database["poi"].find(
            {"is_active": True, "latitude": {"$type": "number"}, "longitude": {"$type": "number"}},
            {"_id": 1, "latitude": 1, "longitude": 1, "image_url": 1, "image_source_url": 1, "source_url": 1, "coordinate_source_url": 1, "coordinate_status": 1},
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
                "translation_review_status": 1,
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
                image_url=poi.get("image_url"),
                image_source_url=poi.get("image_source_url"),
                source_url=poi.get("source_url"),
                coordinate_source_url=poi.get("coordinate_source_url"),
                coordinate_status=poi.get("coordinate_status"),
                translation_review_status=localizations[poi["_id"]].get("translation_review_status"),
            )
            for poi in pois
            if poi["_id"] in localizations
        ]

    async def list_animal_catalog(self, language: str) -> list[AnimalCatalogResponse]:
        poi_cursor = self._database["poi"].find(
            {"source_url": {"$type": "string"}, "candidate_code": {"$type": "string"}},
            {"_id": 1, "candidate_code": 1, "scientific_name": 1, "source_url": 1, "image_url": 1, "image_source_url": 1, "is_active": 1},
        )
        animals = [animal async for animal in poi_cursor]
        if not animals:
            return []

        localizations_cursor = self._database["poi_localizations"].find(
            {"poi_id": {"$in": [animal["_id"] for animal in animals]}, "language_code": language},
            {"_id": 0, "poi_id": 1, "title": 1, "description": 1},
        )
        localized = {item["poi_id"]: item async for item in localizations_cursor}
        return [
            AnimalCatalogResponse(
                id=str(animal["_id"]),
                candidate_code=animal["candidate_code"],
                scientific_name=animal["scientific_name"],
                name=localized[animal["_id"]]["title"],
                description=localized[animal["_id"]]["description"],
                source_url=animal["source_url"],
                map_available=bool(animal.get("is_active")),
                image_url=animal.get("image_url"),
                image_source_url=animal.get("image_source_url"),
            )
            for animal in animals
            if animal["_id"] in localized
        ]
