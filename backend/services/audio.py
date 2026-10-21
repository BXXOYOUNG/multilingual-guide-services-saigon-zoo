from datetime import datetime, timezone
import asyncio
import inspect
from contextlib import asynccontextmanager
from typing import Any, Optional

from bson import ObjectId
from fastapi import HTTPException
from pymongo.asynchronous.database import AsyncDatabase

from backend.repositories.audio import AudioRepository
from backend.schemas.audio import (
    AudioAssetCreate,
    AudioAssetResponse,
    AudioPackageCreate,
    AudioPackageManifest,
    AudioPackageResponse,
    AudioTaskCreate,
    AudioTaskResponse,
    AudioTaskStatus,
    PackageIntegrityStatus,
)
from backend.services.audio_storage import (
    AudioStorageProvider,
    UnconfiguredAudioStorageProvider,
)

TASK_TRANSITIONS = {
    AudioTaskStatus.PENDING: {
        AudioTaskStatus.PROCESSING,
        AudioTaskStatus.FAILED,
    },
    AudioTaskStatus.PROCESSING: {
        AudioTaskStatus.COMPLETED,
        AudioTaskStatus.FAILED,
    },
    AudioTaskStatus.COMPLETED: set(),
    AudioTaskStatus.FAILED: set(),
}
_ASSET_REGISTRATION_LOCKS: dict[
    tuple[str, str, str],
    tuple[asyncio.Lock, int],
] = {}


@asynccontextmanager
async def _serialize_asset_registration(key: tuple[str, str, str]):
    registration = _ASSET_REGISTRATION_LOCKS.get(key)
    lock, users = registration if registration is not None else (asyncio.Lock(), 0)
    _ASSET_REGISTRATION_LOCKS[key] = (lock, users + 1)
    try:
        async with lock:
            yield
    finally:
        current_lock, current_users = _ASSET_REGISTRATION_LOCKS[key]
        if current_users == 1:
            del _ASSET_REGISTRATION_LOCKS[key]
        else:
            _ASSET_REGISTRATION_LOCKS[key] = (
                current_lock,
                current_users - 1,
            )


def parse_object_id(value: str, resource: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=400, detail=f"Invalid {resource} ID")
    return ObjectId(value)


class AudioService:
    def __init__(
        self,
        database: AsyncDatabase,
        storage: Optional[AudioStorageProvider] = None,
    ):
        self.repository = AudioRepository(database)
        self.storage = storage or UnconfiguredAudioStorageProvider()

    async def create_task(self, request: AudioTaskCreate) -> AudioTaskResponse:
        now = datetime.now(timezone.utc)
        document = await self.repository.create_task(
            {
                "poi_id": ObjectId(request.poi_id),
                "language_code": request.language_code,
                "type": request.type.value,
                "status": AudioTaskStatus.PENDING.value,
                "file_url": None,
                "created_at": now,
                "updated_at": now,
            }
        )
        return self._task_response(document)

    async def get_task(self, task_id: str) -> AudioTaskResponse:
        document = await self.repository.get_task(
            parse_object_id(task_id, "audio task")
        )
        if document is None:
            raise HTTPException(status_code=404, detail="Audio task not found")
        self._stored_task_status(document)
        return self._task_response(document)

    async def update_task(
        self,
        task_id: str,
        status: AudioTaskStatus,
        file_url: Optional[str],
        update_file_url: bool,
    ) -> AudioTaskResponse:
        object_id = parse_object_id(task_id, "audio task")
        document = await self.repository.get_task(object_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Audio task not found")

        current = self._stored_task_status(document)
        if status != current and status not in TASK_TRANSITIONS[current]:
            raise HTTPException(
                status_code=409,
                detail=f"Cannot transition audio task from {current.value} "
                f"to {status.value}",
            )
        if status == current and not update_file_url:
            return self._task_response(document)

        updates: dict[str, Any] = {
            "status": status.value,
            "updated_at": datetime.now(timezone.utc),
        }
        if update_file_url:
            updates["file_url"] = file_url
        updated = await self.repository.update_task(
            object_id,
            current.value,
            updates,
        )
        if not updated:
            raise HTTPException(
                status_code=409,
                detail="Audio task changed during the update",
            )
        document.update(updates)
        return self._task_response(document)

    async def create_package(
        self,
        request: AudioPackageCreate,
    ) -> AudioPackageResponse:
        document = await self.repository.create_package(
            {
                "name": request.name,
                "language_code": request.language_code,
                "description": request.description,
                "file_url": request.file_url,
                "file_size": request.file_size,
                "is_offline": request.is_offline,
                "created_at": datetime.now(timezone.utc),
            }
        )
        return await self._package_response(document)

    async def get_package_manifest(
        self,
        package_id: str,
    ) -> AudioPackageManifest:
        object_id = parse_object_id(package_id, "audio package")
        package = await self.repository.get_package(object_id)
        if package is None:
            raise HTTPException(status_code=404, detail="Audio package not found")

        documents = await self.repository.list_package_assets(object_id)
        if any(
            asset["language_code"] != package["language_code"]
            for asset in documents
        ):
            raise HTTPException(
                status_code=409,
                detail="Audio package contains an asset in another language",
            )

        errors: list[str] = []
        # Audio packages are logical manifests assembled from their stored assets;
        # package.file_url is metadata, not a second archive to download.
        unverified = False

        assets: list[AudioAssetResponse] = []
        for asset in documents:
            info = await self.storage.inspect(asset["file_url"])
            if info is None or info.checksum is None:
                unverified = True
            elif info.checksum.lower() != asset["checksum"].lower():
                errors.append(
                    f"Audio asset {asset['_id']} checksum does not match"
                )
            if info is not None and asset.get("size_bytes") is not None and info.size != asset["size_bytes"]:
                errors.append(f"Audio asset {asset['_id']} size does not match")
            assets.append(await self._asset_response(asset))

        integrity_status = (
            PackageIntegrityStatus.INVALID
            if errors
            else PackageIntegrityStatus.UNVERIFIED
            if unverified
            else PackageIntegrityStatus.VERIFIED
        )
        return AudioPackageManifest(
            package=await self._package_response(package),
            assets=assets,
            integrity_status=integrity_status,
            integrity_errors=errors,
        )

    async def create_asset(
        self,
        request: AudioAssetCreate,
    ) -> AudioAssetResponse:
        poi_id = ObjectId(request.poi_id)
        package_id = (
            ObjectId(request.package_id) if request.package_id is not None else None
        )
        if package_id is not None:
            package = await self.repository.get_package(package_id)
            if package is None:
                raise HTTPException(
                    status_code=404,
                    detail="Audio package not found",
                )
            if package["language_code"] != request.language_code:
                raise HTTPException(
                    status_code=409,
                    detail="Audio asset language must match its package",
                )

        document = {
            "package_id": package_id,
            "poi_id": poi_id,
            "language_code": request.language_code,
            "file_url": request.file_url,
            "duration": request.duration,
            "checksum": request.checksum,
            "created_at": datetime.now(timezone.utc),
        }
        created_asset = await self._register_asset(document)
        if not created_asset:
            duplicate = await self.repository.find_asset_by_checksum(
                poi_id,
                request.language_code,
                request.checksum,
            )
            if duplicate is None:
                raise RuntimeError("Duplicate audio asset disappeared")
            document = duplicate
        return await self._asset_response(document)

    async def _register_asset(self, document: dict[str, Any]) -> bool:
        lock_key = (
            str(document["poi_id"]),
            document["language_code"],
            document["checksum"],
        )
        async with _serialize_asset_registration(lock_key):
            return await self._register_asset_locked(document)

    async def _register_asset_locked(self, document: dict[str, Any]) -> bool:
        client = getattr(self.repository.database, "client", None)
        start_session = getattr(client, "start_session", None)
        if not callable(start_session):
            return await self._register_asset_with_compensation(document)

        try:
            session = start_session()
            if inspect.isawaitable(session):
                session = await session
            async with session:
                transaction = session.start_transaction()
                if inspect.isawaitable(transaction):
                    transaction = await transaction

                async with transaction:
                    return await self._register_asset_in_transaction(
                        document,
                        session,
                    )
        except Exception as error:
            if not self._transactions_unsupported(error):
                raise
        return await self._register_asset_with_compensation(document)

    async def _register_asset_in_transaction(
        self,
        document: dict[str, Any],
        session: Any,
    ) -> bool:
        localization = await self.repository.get_localization(
            document["poi_id"],
            document["language_code"],
            session=session,
        )
        if localization is None:
            raise HTTPException(
                status_code=404,
                detail="POI localization not found for the requested language",
            )

        duplicate = await self.repository.find_asset_by_checksum(
            document["poi_id"],
            document["language_code"],
            document["checksum"],
            session=session,
        )
        if duplicate is not None:
            self._validate_duplicate(document, duplicate)

            if localization.get("audio_url") != document["file_url"]:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "POI localization points to a different audio asset"
                    ),
                )
            return False

        asset = await self.repository.create_asset(document, session=session)
        if not await self.repository.set_localization_audio(
            document["poi_id"],
            document["language_code"],
            document["file_url"],
            localization.get("audio_url"),
            "audio_url" in localization,
            session=session,
        ):
            raise HTTPException(
                status_code=409,
                detail="POI localization changed during audio registration",
            )
        document["_id"] = asset["_id"]
        return True

    async def _register_asset_with_compensation(
        self,
        document: dict[str, Any],
    ) -> bool:
        poi_id = document["poi_id"]
        language_code = document["language_code"]
        localization = await self.repository.get_localization(
            poi_id,
            language_code,
        )
        if localization is None:
            raise HTTPException(
                status_code=404,
                detail="POI localization not found for the requested language",
            )

        duplicate = await self.repository.find_asset_by_checksum(
            poi_id,
            language_code,
            document["checksum"],
        )
        if duplicate is not None:
            self._validate_duplicate(document, duplicate)

            if localization.get("audio_url") != document["file_url"]:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "POI localization points to a different audio asset"
                    ),
                )

            document.clear()
            document.update(duplicate)
            return False

        asset = await self.repository.create_asset(document)
        try:
            matched = await self.repository.set_localization_audio(
                poi_id,
                language_code,
                document["file_url"],
                localization.get("audio_url"),
                "audio_url" in localization,
            )
        except Exception as error:
            raise RuntimeError(
                "POI localization update outcome is unknown; the audio asset "
                "was retained. Inspect the localization before retrying or "
                "cleaning up the asset."
            ) from error

        if not matched:
            current = await self.repository.get_localization(
                poi_id,
                language_code,
            )
            if current is not None:
                if current.get("audio_url") == document["file_url"]:
                    document["_id"] = asset["_id"]
                    return True
                raise HTTPException(
                    status_code=409,
                    detail="POI localization changed during audio registration; "
                    "the asset was retained to avoid breaking a concurrent update",
                )
            raise HTTPException(
                status_code=404,
                detail="POI localization disappeared during audio registration; "
                "the asset was retained for retry or cleanup",
            )
        document["_id"] = asset["_id"]
        return True

    @staticmethod
    def _validate_duplicate(
        requested: dict[str, Any],
        existing: dict[str, Any],
    ) -> None:
        """Treat exact checksum replays as idempotent; reject metadata conflicts."""
        matching_fields = (
            "package_id",
            "poi_id",
            "language_code",
            "file_url",
            "duration",
            "checksum",
        )
        if any(requested[field] != existing.get(field) for field in matching_fields):
            raise HTTPException(
                status_code=409,
                detail="Audio asset checksum is already registered with "
                "different metadata",
            )

    @staticmethod
    def _transactions_unsupported(error: Exception) -> bool:
        return (
            getattr(error, "code", None) == 20
            and "Transaction numbers are only allowed on a replica set member "
            "or mongos" in str(error)
        )

    @staticmethod
    def _stored_task_status(document: dict[str, Any]) -> AudioTaskStatus:
        try:
            return AudioTaskStatus(document["status"])
        except (KeyError, ValueError) as error:
            raise HTTPException(
                status_code=409,
                detail="Audio task has an invalid stored status",
            ) from error

    async def get_ready_asset(
        self,
        poi_id: str,
        language_code: str,
    ) -> AudioAssetResponse:
        document = await self.repository.get_ready_asset(
            parse_object_id(poi_id, "POI"),
            language_code,
        )
        if document is None:
            raise HTTPException(status_code=404, detail="Ready audio asset not found")
        return await self._asset_response(document)

    async def read_asset(self, asset_id: str) -> tuple[bytes, str]:
        object_id = parse_object_id(asset_id, "audio asset")
        document = await self.repository.get_asset(object_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Audio asset not found")
        result = await self.storage.read(document["file_url"])
        if result is None:
            raise HTTPException(status_code=404, detail="Audio object not found")
        return result

    async def assign_asset(
        self,
        package_id: str,
        asset_id: str,
    ) -> AudioPackageManifest:
        package_object_id = parse_object_id(package_id, "audio package")
        asset_object_id = parse_object_id(asset_id, "audio asset")
        package = await self.repository.get_package(package_object_id)
        if package is None:
            raise HTTPException(status_code=404, detail="Audio package not found")
        asset = await self.repository.get_asset(asset_object_id)
        if asset is None:
            raise HTTPException(status_code=404, detail="Audio asset not found")
        if asset["language_code"] != package["language_code"]:
            raise HTTPException(
                status_code=409,
                detail="Audio asset language must match its package",
            )
        if not await self.repository.assign_asset_to_package(
            asset_object_id,
            package_object_id,
        ):
            raise HTTPException(status_code=404, detail="Audio asset not found")
        return await self.get_package_manifest(str(package_object_id))

    async def _package_response(
        self,
        document: dict[str, Any],
    ) -> AudioPackageResponse:
        return AudioPackageResponse(
            id=str(document["_id"]),
            name=document["name"],
            language_code=document["language_code"],
            description=document["description"],
            file_url=document["file_url"],
            download_url=await self.storage.get_access_url(document["file_url"]),
            file_size=document["file_size"],
            is_offline=document["is_offline"],
            created_at=document["created_at"],
        )

    async def _asset_response(
        self,
        document: dict[str, Any],
    ) -> AudioAssetResponse:
        metadata = await self.storage.inspect(document["file_url"])
        return AudioAssetResponse(
            id=str(document["_id"]),
            package_id=(
                str(document["package_id"])
                if document.get("package_id") is not None
                else None
            ),
            poi_id=str(document["poi_id"]),
            language_code=document["language_code"],
            file_url=document["file_url"],
            playback_url=await self.storage.get_access_url(document["file_url"]),
            size_bytes=metadata.size if metadata else None,
            duration=document["duration"],
            checksum=document["checksum"],
            created_at=document["created_at"],
        )

    @staticmethod
    def _task_response(document: dict[str, Any]) -> AudioTaskResponse:
        return AudioTaskResponse(
            id=str(document["_id"]),
            poi_id=str(document["poi_id"]),
            language_code=document["language_code"],
            type=document["type"],
            status=document["status"],
            file_url=document.get("file_url"),
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )
