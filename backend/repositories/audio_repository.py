from typing import Optional
from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from backend.integrations.storage.storage_adapter import StorageAdapter, LocalStorageAdapter
from backend.schemas.audio import (
    AudioAssetResponse,
    AudioPackageResponse,
    AudioPackageManifest,
    AudioPackageStatus,
    AudioTaskResponse,
    AudioTaskStatus,
)


class AudioRepository:
    """
    Data access layer for audio assets, audio packages, and audio tasks.
    Adheres strictly to section 5.2, 5.6, and 11.1 of IMPLEMENTATION_PLAN.md.
    """

    def __init__(
        self,
        database: AsyncDatabase,
        storage_adapter: Optional[StorageAdapter] = None,
    ) -> None:
        self._database = database
        self._storage = storage_adapter or LocalStorageAdapter()

    def _to_object_id(self, val: str) -> ObjectId | str:
        if ObjectId.is_valid(val):
            return ObjectId(val)
        return val

    # --- Audio Asset Operations ---

    async def get_asset_by_id(self, asset_id: str) -> Optional[AudioAssetResponse]:
        doc = await self._database["audio_assets"].find_one({"_id": self._to_object_id(asset_id)})
        if not doc:
            return None
        return self._format_asset(doc)

    async def get_asset_by_poi_and_language(
        self, poi_id: str, language_code: str
    ) -> Optional[AudioAssetResponse]:
        doc = await self._database["audio_assets"].find_one({
            "poi_id": self._to_object_id(poi_id),
            "language_code": language_code,
        })
        if not doc:
            return None
        return self._format_asset(doc)

    async def list_assets_by_package_id(self, package_id: str) -> list[AudioAssetResponse]:
        cursor = self._database["audio_assets"].find({
            "package_id": self._to_object_id(package_id),
        })
        return [self._format_asset(doc) async for doc in cursor]

    def _format_asset(self, doc: dict) -> AudioAssetResponse:
        file_path = doc.get("file_path", "")
        # poi_localizations.audio_url or generated storage public url
        audio_url = doc.get("audio_url") or self._storage.get_public_url(file_path)
        return AudioAssetResponse(
            id=str(doc["_id"]),
            poi_id=str(doc.get("poi_id", "")),
            language_code=doc.get("language_code", ""),
            package_id=str(doc["package_id"]) if doc.get("package_id") is not None else None,
            file_path=file_path,
            audio_url=audio_url,
            duration_seconds=float(doc.get("duration_seconds", 0.0)),
            file_size_bytes=int(doc.get("file_size_bytes", 0)),
            format=doc.get("format", "mp3"),
            checksum=doc.get("checksum"),
        )

    # --- Audio Package Operations ---

    async def get_package_by_id(self, package_id: str) -> Optional[AudioPackageResponse]:
        doc = await self._database["audio_packages"].find_one({"_id": self._to_object_id(package_id)})
        if not doc:
            return None
        return self._format_package(doc)

    async def get_ready_package_by_language(
        self, language_code: str
    ) -> Optional[AudioPackageResponse]:
        doc = await self._database["audio_packages"].find_one({
            "language_code": language_code,
            "status": AudioPackageStatus.READY.value,
        })
        if not doc:
            return None
        return self._format_package(doc)

    async def get_package_manifest(self, package_id: str) -> Optional[AudioPackageManifest]:
        package = await self.get_package_by_id(package_id)
        if not package:
            return None

        assets = await self.list_assets_by_package_id(package_id)
        return AudioPackageManifest(
            package_id=package.id,
            package_name=package.package_name,
            language_code=package.language_code,
            version=package.version,
            status=package.status,
            total_assets=package.total_assets,
            total_size_bytes=package.total_size_bytes,
            download_url=package.download_url,
            checksum=package.checksum,
            assets=assets,
        )

    def _format_package(self, doc: dict) -> AudioPackageResponse:
        download_url = doc.get("download_url")
        if not download_url and doc.get("file_path"):
            download_url = self._storage.get_public_url(doc["file_path"])

        return AudioPackageResponse(
            id=str(doc["_id"]),
            package_name=doc.get("package_name", "Gói thuyết minh Thảo Cầm Viên"),
            language_code=doc.get("language_code", ""),
            version=doc.get("version", "1.0.0"),
            status=AudioPackageStatus(doc.get("status", AudioPackageStatus.DRAFT.value)),
            total_assets=int(doc.get("total_assets", 0)),
            total_size_bytes=int(doc.get("total_size_bytes", 0)),
            download_url=download_url,
            checksum=doc.get("checksum"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
        )

    # --- Audio Task Operations ---

    async def get_task_by_id(self, task_id: str) -> Optional[AudioTaskResponse]:
        doc = await self._database["audio_tasks"].find_one({"_id": self._to_object_id(task_id)})
        if not doc:
            return None
        return self._format_task(doc)

    async def get_latest_task_for_poi(
        self, poi_id: str, language_code: str
    ) -> Optional[AudioTaskResponse]:
        doc = await self._database["audio_tasks"].find_one(
            {
                "poi_id": self._to_object_id(poi_id),
                "language_code": language_code,
            },
            sort=[("created_at", -1)],
        )
        if not doc:
            return None
        return self._format_task(doc)

    def _format_task(self, doc: dict) -> AudioTaskResponse:
        return AudioTaskResponse(
            id=str(doc["_id"]),
            poi_id=str(doc.get("poi_id", "")),
            language_code=doc.get("language_code", ""),
            status=AudioTaskStatus(doc.get("status", AudioTaskStatus.PENDING.value)),
            error_message=doc.get("error_message"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
        )

