from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.asynchronous.database import AsyncDatabase

from backend.database.mongodb import get_database
from backend.repositories.audio_repository import AudioRepository
from backend.schemas.audio import (
    AudioAssetResponse,
    AudioPackageResponse,
    AudioPackageManifest,
    AudioTaskResponse,
)

router = APIRouter(prefix="/api/audio", tags=["audio"])


def get_audio_repository() -> AudioRepository:
    database: AsyncDatabase = get_database()
    return AudioRepository(database)


# --- 1. Audio Assets APIs ---

@router.get("/assets", response_model=AudioAssetResponse)
async def get_audio_asset_by_poi(
    poi_id: str = Query(..., min_length=1, description="ID của POI"),
    language: str = Query(..., min_length=1, description="Mã ngôn ngữ (e.g. vi, en)"),
    repository: AudioRepository = Depends(get_audio_repository),
) -> AudioAssetResponse:
    """
    Lấy thông tin và audio_url phát trực tiếp cho một POI theo ngôn ngữ.
    """
    asset = await repository.get_asset_by_poi_and_language(poi_id, language)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy audio asset cho POI {poi_id} với ngôn ngữ '{language}'",
        )
    return asset


@router.get("/assets/{asset_id}", response_model=AudioAssetResponse)
async def get_audio_asset(
    asset_id: str,
    repository: AudioRepository = Depends(get_audio_repository),
) -> AudioAssetResponse:
    """
    Lấy metadata của một audio asset theo ID.
    """
    asset = await repository.get_asset_by_id(asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy audio asset với ID {asset_id}",
        )
    return asset


# --- 2. Audio Packages APIs (phục vụ UC-05 / UC-06) ---

@router.get("/packages", response_model=AudioPackageResponse)
async def get_audio_package_by_language(
    language: str = Query(..., min_length=1, description="Mã ngôn ngữ của gói audio"),
    repository: AudioRepository = Depends(get_audio_repository),
) -> AudioPackageResponse:
    """
    Lấy metadata của gói audio offline sẵn sàng (ready) cho ngôn ngữ được chọn.
    """
    package = await repository.get_ready_package_by_language(language)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không có gói audio offline sẵn sàng cho ngôn ngữ '{language}'",
        )
    return package


@router.get("/packages/{package_id}", response_model=AudioPackageResponse)
async def get_audio_package(
    package_id: str,
    repository: AudioRepository = Depends(get_audio_repository),
) -> AudioPackageResponse:
    """
    Lấy thông tin gói audio offline theo package_id.
    """
    package = await repository.get_package_by_id(package_id)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy gói audio với ID {package_id}",
        )
    return package


@router.get("/packages/{package_id}/manifest", response_model=AudioPackageManifest)
async def get_audio_package_manifest(
    package_id: str,
    repository: AudioRepository = Depends(get_audio_repository),
) -> AudioPackageManifest:
    """
    Lấy manifest chi tiết của gói audio offline gồm danh sách toàn bộ audio asset để client tải về.
    """
    manifest = await repository.get_package_manifest(package_id)
    if not manifest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy manifest cho gói audio {package_id}",
        )
    return manifest


# --- 3. Audio Tasks APIs ---

@router.get("/tasks/{task_id}", response_model=AudioTaskResponse)
async def get_audio_task(
    task_id: str,
    repository: AudioRepository = Depends(get_audio_repository),
) -> AudioTaskResponse:
    """
    Kiểm tra trạng thái của tác vụ xử lý audio (audio_task).
    """
    task = await repository.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy audio task với ID {task_id}",
        )
    return task

