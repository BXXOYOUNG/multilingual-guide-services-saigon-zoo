import os
from functools import lru_cache
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
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
from backend.services.audio_storage import (
    AudioStorageProvider,
    S3CompatibleAudioStorageProvider,
    UnconfiguredAudioStorageProvider,
)
from backend.services.admin_auth import require_permission

router = APIRouter(prefix="/audio", tags=["audio"])

# Optional override for tests or explicit dependency injection.
_storage_provider: Optional[AudioStorageProvider] = None


@lru_cache(maxsize=8)
def _build_s3_storage_provider(
    endpoint_url: str,
    bucket: str,
    access_key_id: str,
    secret_access_key: str,
    region_name: str,
    expires_in: int,
) -> S3CompatibleAudioStorageProvider:
    return S3CompatibleAudioStorageProvider(
        endpoint_url=endpoint_url,
        bucket=bucket,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        region_name=region_name,
        presigned_url_expires_in=expires_in,
    )


def get_audio_storage_provider() -> AudioStorageProvider:
    if _storage_provider is not None:
        return _storage_provider

    endpoint_url = os.getenv("AUDIO_STORAGE_ENDPOINT_URL", "").strip()
    bucket = os.getenv("AUDIO_STORAGE_BUCKET", "").strip()
    access_key_id = os.getenv("AUDIO_STORAGE_ACCESS_KEY_ID", "").strip()
    secret_access_key = os.getenv(
        "AUDIO_STORAGE_SECRET_ACCESS_KEY", ""
    ).strip()

    configured_values = {
        "AUDIO_STORAGE_ENDPOINT_URL": endpoint_url,
        "AUDIO_STORAGE_BUCKET": bucket,
        "AUDIO_STORAGE_ACCESS_KEY_ID": access_key_id,
        "AUDIO_STORAGE_SECRET_ACCESS_KEY": secret_access_key,
    }

    # Keep existing behavior when storage has not been configured.
    if not any(configured_values.values()):
        return UnconfiguredAudioStorageProvider()

    missing = [
        name for name, value in configured_values.items() if not value
    ]
    if missing:
        raise RuntimeError(
            "Incomplete audio storage configuration; missing: "
            + ", ".join(missing)
        )

    region_name = os.getenv("AUDIO_STORAGE_REGION", "us-east-1").strip()
    try:
        expires_in = int(
            os.getenv("AUDIO_STORAGE_PRESIGNED_URL_EXPIRES_IN", "300")
        )
    except ValueError as error:
        raise RuntimeError(
            "AUDIO_STORAGE_PRESIGNED_URL_EXPIRES_IN must be an integer"
        ) from error

    return _build_s3_storage_provider(
        endpoint_url,
        bucket,
        access_key_id,
        secret_access_key,
        region_name,
        expires_in,
    )


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
    _admin=Depends(require_permission("audio:write")),
    service: AudioService = Depends(get_audio_service),
) -> AudioTaskResponse:
    return await service.create_task(request)


@router.get("/tasks/{task_id}", response_model=AudioTaskResponse)
async def get_audio_task(
    task_id: str,
    _admin=Depends(require_permission("audio:write")),
    service: AudioService = Depends(get_audio_service),
) -> AudioTaskResponse:
    return await service.get_task(task_id)


@router.patch("/tasks/{task_id}/status", response_model=AudioTaskResponse)
async def update_audio_task_status(
    task_id: str,
    request: AudioTaskStatusUpdate,
    _admin=Depends(require_permission("audio:write")),
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
    _admin=Depends(require_permission("audio:write")),
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
    _admin=Depends(require_permission("audio:write")),
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
    _admin=Depends(require_permission("audio:write")),
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


@router.get("/assets/{asset_id}/content")
async def stream_audio_asset(
    asset_id: str,
    service: AudioService = Depends(get_audio_service),
) -> Response:
    content, media_type = await service.read_asset(asset_id)
    return Response(
        content=content,
        media_type=media_type,
        headers={"Cache-Control": "public, max-age=86400"},
    )
