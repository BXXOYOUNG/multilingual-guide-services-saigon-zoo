from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AudioTaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AudioPackageStatus(str, Enum):
    DRAFT = "draft"
    BUILDING = "building"
    READY = "ready"
    FAILED = "failed"


class AudioAssetResponse(BaseModel):
    id: str
    poi_id: str
    language_code: str
    package_id: Optional[str] = None
    file_path: str
    audio_url: str
    duration_seconds: float
    file_size_bytes: int
    format: str = "mp3"
    checksum: Optional[str] = None


class AudioPackageResponse(BaseModel):
    id: str
    package_name: str
    language_code: str
    version: str
    status: AudioPackageStatus
    total_assets: int
    total_size_bytes: int
    download_url: Optional[str] = None
    checksum: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AudioPackageManifest(BaseModel):
    package_id: str
    package_name: str
    language_code: str
    version: str
    status: AudioPackageStatus
    total_assets: int
    total_size_bytes: int
    download_url: Optional[str] = None
    checksum: Optional[str] = None
    assets: list[AudioAssetResponse] = Field(default_factory=list)


class AudioTaskResponse(BaseModel):
    id: str
    poi_id: str
    language_code: str
    status: AudioTaskStatus
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

