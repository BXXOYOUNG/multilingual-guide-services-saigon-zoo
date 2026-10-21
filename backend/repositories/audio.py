from typing import Any, Optional

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase


class AudioRepository:
    def __init__(self, database: AsyncDatabase):
        self.database = database

    async def create_task(self, document: dict[str, Any]) -> dict[str, Any]:
        result = await self.database["audio_tasks"].insert_one(document)
        return {**document, "_id": result.inserted_id}

    async def get_task(self, task_id: ObjectId) -> Optional[dict[str, Any]]:
        return await self.database["audio_tasks"].find_one({"_id": task_id})

    async def update_task(
        self,
        task_id: ObjectId,
        current_status: str,
        updates: dict[str, Any],
    ) -> bool:
        result = await self.database["audio_tasks"].update_one(
            {"_id": task_id, "status": current_status},
            {"$set": updates},
        )
        return result.matched_count == 1

    async def create_package(self, document: dict[str, Any]) -> dict[str, Any]:
        result = await self.database["audio_packages"].insert_one(document)
        return {**document, "_id": result.inserted_id}

    async def get_package(
        self,
        package_id: ObjectId,
    ) -> Optional[dict[str, Any]]:
        return await self.database["audio_packages"].find_one(
            {"_id": package_id}
        )

    async def list_package_assets(
        self,
        package_id: ObjectId,
    ) -> list[dict[str, Any]]:
        cursor = self.database["audio_assets"].find(
            {"package_id": package_id}
        )
        return await cursor.to_list(length=None)

    async def get_asset(self, asset_id: ObjectId) -> Optional[dict[str, Any]]:
        return await self.database["audio_assets"].find_one({"_id": asset_id})

    async def get_ready_asset(
        self,
        poi_id: ObjectId,
        language_code: str,
    ) -> Optional[dict[str, Any]]:
        localization = await self.get_localization(poi_id, language_code)
        if not localization or not localization.get("audio_url"):
            return None
        return await self.database["audio_assets"].find_one(
            {"poi_id": poi_id, "language_code": language_code, "file_url": localization["audio_url"]},
            sort=[("created_at", -1)],
        )

    async def get_localization(
        self,
        poi_id: ObjectId,
        language_code: str,
        session: Any = None,
    ) -> Optional[dict[str, Any]]:
        return await self.database["poi_localizations"].find_one(
            {"poi_id": poi_id, "language_code": language_code},
            session=session,
        )

    async def find_asset_by_checksum(
        self,
        poi_id: ObjectId,
        language_code: str,
        checksum: str,
        session: Any = None,
    ) -> Optional[dict[str, Any]]:
        return await self.database["audio_assets"].find_one(
            {
                "poi_id": poi_id,
                "language_code": language_code,
                "checksum": checksum,
            },
            session=session,
        )

    async def create_asset(
        self,
        document: dict[str, Any],
        session: Any = None,
    ) -> dict[str, Any]:
        result = await self.database["audio_assets"].insert_one(
            document,
            session=session,
        )
        return {**document, "_id": result.inserted_id}

    async def set_localization_audio(
        self,
        poi_id: ObjectId,
        language_code: str,
        file_url: str,
        expected_audio_url: Any,
        audio_url_present: bool,
        session: Any = None,
    ) -> bool:
        query: dict[str, Any] = {
            "poi_id": poi_id,
            "language_code": language_code,
        }
        if audio_url_present:
            query["audio_url"] = expected_audio_url
        else:
            query["audio_url"] = {"$exists": False}
        result = await self.database["poi_localizations"].update_one(
            query,
            {"$set": {"audio_url": file_url}},
            session=session,
        )
        return result.matched_count == 1

    async def assign_asset_to_package(
        self,
        asset_id: ObjectId,
        package_id: ObjectId,
    ) -> bool:
        result = await self.database["audio_assets"].update_one(
            {"_id": asset_id},
            {"$set": {"package_id": package_id}},
        )
        return result.matched_count == 1
