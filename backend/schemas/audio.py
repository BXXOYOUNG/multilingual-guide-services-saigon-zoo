from datetime import datetime
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator


class AudioTaskType(str, Enum):
    TTS = "TTS"
    MANUAL = "Manual"


class AudioTaskStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"


class PackageIntegrityStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    INVALID = "invalid"


def _validate_object_id(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError("Must be a valid MongoDB ObjectId")
    return value


def _validate_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Must not be empty")
    return value


class AudioTaskCreate(BaseModel):
    poi_id: str
    language_code: str
    type: AudioTaskType

    _poi_id = field_validator("poi_id")(_validate_object_id)
    _language_code = field_validator("language_code")(_validate_text)


class AudioTaskStatusUpdate(BaseModel):
    status: AudioTaskStatus
    file_url: Optional[str] = None

    @field_validator("file_url")
    @classmethod
    def validate_file_url(cls, value: Optional[str]) -> Optional[str]:
        return None if value is None else _validate_text(value)


class AudioTaskResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    poi_id: str
    language_code: str
    type: AudioTaskType
    status: AudioTaskStatus
    file_url: Optional[str]
    created_at: datetime
    updated_at: datetime


class AudioAssetCreate(BaseModel):
    package_id: Optional[str] = None
    poi_id: str
    language_code: str
    file_url: str
    duration: float = Field(ge=0)
    checksum: str

    _package_id = field_validator("package_id")(
        lambda value: None if value is None else _validate_object_id(value)
    )
    _poi_id = field_validator("poi_id")(_validate_object_id)
    _language_code = field_validator("language_code")(_validate_text)
    _file_url = field_validator("file_url")(_validate_text)
    _checksum = field_validator("checksum")(_validate_text)


class AudioAssetResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    package_id: Optional[str]
    poi_id: str
    language_code: str
    file_url: str
    playback_url: Optional[str]
    duration: float
    checksum: str
    created_at: datetime


class AudioPackageCreate(BaseModel):
    name: str
    language_code: str
    description: str
    file_url: str
    file_size: int = Field(ge=0)
    is_offline: bool

    _name = field_validator("name")(_validate_text)
    _language_code = field_validator("language_code")(_validate_text)
    _description = field_validator("description")(_validate_text)
    _file_url = field_validator("file_url")(_validate_text)


class AudioPackageResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    name: str
    language_code: str
    description: str
    file_url: str
    download_url: Optional[str] = None
    file_size: int
    is_offline: bool
    created_at: datetime


class AudioPackageManifest(BaseModel):
    package: AudioPackageResponse
    assets: list[AudioAssetResponse]
    integrity_status: PackageIntegrityStatus
    integrity_errors: list[str] = Field(default_factory=list)
