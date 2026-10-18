from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from pymongo.asynchronous.database import AsyncDatabase

from backend.database.mongodb import get_database
from backend.schemas.audio import (
    AudioAssetCreate,
    AudioAssetResponse,
    AudioPackageCreate,
    AudioPackageManifest,
    AudioPackageResponse,
    AudioTaskCreate,
    AudioTaskResponse,
    AudioTaskStatusUpdate,
)
from backend.services.audio import AudioService
from backend.services.audio_storage import AudioStorageProvider

router = APIRouter(prefix="/audio", tags=["audio"])
_storage_provider: Optional[AudioStorageProvider] = None


def get_audio_storage_provider() -> AudioStorageProvider:
    if _storage_provider is None:
        from backend.services.audio_storage import UnconfiguredAudioStorageProvider

        return UnconfiguredAudioStorageProvider()
    return _storage_provider


def get_audio_service(
    database: AsyncDatabase = Depends(get_database),
    storage: AudioStorageProvider = Depends(get_audio_storage_provider),
) -> AudioService:
    return AudioService(database, storage)


@router.post(
    "/tasks",
    response_model=AudioTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_audio_task(
    request: AudioTaskCreate,
    service: AudioService = Depends(get_audio_service),
) -> AudioTaskResponse:
    return await service.create_task(request)


@router.get("/tasks/{task_id}", response_model=AudioTaskResponse)
async def get_audio_task(
    task_id: str,
    service: AudioService = Depends(get_audio_service),
) -> AudioTaskResponse:
    return await service.get_task(task_id)


@router.patch("/tasks/{task_id}/status", response_model=AudioTaskResponse)
async def update_audio_task_status(
    task_id: str,
    request: AudioTaskStatusUpdate,
    service: AudioService = Depends(get_audio_service),
) -> AudioTaskResponse:
    return await service.update_task(
        task_id,
        request.status,
        request.file_url,
        "file_url" in request.model_fields_set,
    )


@router.post(
    "/packages",
    response_model=AudioPackageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_audio_package(
    request: AudioPackageCreate,
    service: AudioService = Depends(get_audio_service),
) -> AudioPackageResponse:
    return await service.create_package(request)


@router.get(
    "/packages/{package_id}/manifest",
    response_model=AudioPackageManifest,
)
async def get_audio_package_manifest(
    package_id: str,
    service: AudioService = Depends(get_audio_service),
) -> AudioPackageManifest:
    return await service.get_package_manifest(package_id)


@router.post(
    "/packages/{package_id}/assets/{asset_id}",
    response_model=AudioPackageManifest,
)
async def assign_asset_to_audio_package(
    package_id: str,
    asset_id: str,
    service: AudioService = Depends(get_audio_service),
) -> AudioPackageManifest:
    return await service.assign_asset(package_id, asset_id)


@router.post(
    "/assets",
    response_model=AudioAssetResponse,
    status_code=status.HTTP_201_CREATED,
    description=(
        "An exact repeat for the same POI, language, and checksum is idempotent "
        "when package, file URL, and duration also match. Reusing that checksum "
        "with different metadata returns 409. Without MongoDB transactions, "
        "concurrent requests handled by different workers can create duplicates. "
        "If the localization update raises after an asset insert, the outcome "
        "is indeterminate and the asset is retained. A retry is idempotent only "
        "if the localization already points to the same file URL; otherwise, "
        "the API returns an error rather than overwriting a different URL. "
        "Inspect the localization and reconcile the retained asset explicitly. "
        "A localization deleted during fallback update also leaves the asset "
        "for explicit retry or cleanup because cross-collection deletion "
        "cannot be made race-safe without a transaction."
    ),
)
async def create_audio_asset(
    request: AudioAssetCreate,
    service: AudioService = Depends(get_audio_service),
) -> AudioAssetResponse:
    return await service.create_asset(request)


@router.get("/assets/resolve", response_model=AudioAssetResponse)
async def resolve_ready_audio_asset(
    poi_id: str = Query(...),
    language_code: str = Query(..., min_length=1),
    service: AudioService = Depends(get_audio_service),
) -> AudioAssetResponse:
    return await service.get_ready_asset(poi_id, language_code)
