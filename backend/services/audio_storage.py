from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass(frozen=True)
class StorageObjectMetadata:
    size: Optional[int] = None
    checksum: Optional[str] = None


class AudioStorageProvider(Protocol):
    async def get_access_url(self, file_url: str) -> Optional[str]:
        """Return a provider-issued access URL, or None when unavailable."""

    async def inspect(self, file_url: str) -> Optional[StorageObjectMetadata]:
        """Return stored object metadata when the provider can inspect it."""


class UnconfiguredAudioStorageProvider:
    async def get_access_url(self, file_url: str) -> Optional[str]:
        return None

    async def inspect(self, file_url: str) -> Optional[StorageObjectMetadata]:
        return None
