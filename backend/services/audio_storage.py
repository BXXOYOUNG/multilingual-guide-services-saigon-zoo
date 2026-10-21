import asyncio
from dataclasses import dataclass
from typing import Optional, Protocol

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


@dataclass(frozen=True)
class StorageObjectMetadata:
    size: Optional[int] = None
    checksum: Optional[str] = None


class AudioStorageProvider(Protocol):
    async def get_access_url(self, file_url: str) -> Optional[str]:
        """Return a provider-issued access URL, or None when unavailable."""

    async def inspect(self, file_url: str) -> Optional[StorageObjectMetadata]:
        """Return stored object metadata when the provider can inspect it."""

    async def read(self, file_url: str) -> Optional[tuple[bytes, str]]:
        """Read an audio object for same-origin visitor playback/download."""

    async def put(self, file_url: str, content: bytes, media_type: str, checksum: str) -> None:
        """Store an audio object and checksum metadata."""


class UnconfiguredAudioStorageProvider:
    async def get_access_url(self, file_url: str) -> Optional[str]:
        return None

    async def inspect(self, file_url: str) -> Optional[StorageObjectMetadata]:
        return None

    async def read(self, file_url: str) -> Optional[tuple[bytes, str]]:
        return None

    async def put(self, file_url: str, content: bytes, media_type: str, checksum: str) -> None:
        raise RuntimeError("Audio storage is not configured")


class S3CompatibleAudioStorageProvider:
    """S3-compatible storage provider for SeaweedFS or an S3 service."""

    def __init__(
        self,
        *,
        endpoint_url: str,
        bucket: str,
        access_key_id: str,
        secret_access_key: str,
        region_name: str = "us-east-1",
        presigned_url_expires_in: int = 900,
    ) -> None:
        required_values = {
            "endpoint_url": endpoint_url,
            "bucket": bucket,
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
            "region_name": region_name,
        }
        missing = [
            name for name, value in required_values.items()
            if not value or not value.strip()
        ]
        if missing:
            raise ValueError(
                f"Missing S3 storage configuration: {', '.join(missing)}"
            )

        if not 1 <= presigned_url_expires_in <= 604800:
            raise ValueError(
                "presigned_url_expires_in must be between 1 and 604800"
            )

        self.bucket = bucket
        self.presigned_url_expires_in = presigned_url_expires_in

        self._client = boto3.client(
            "s3",
            endpoint_url=endpoint_url.rstrip("/"),
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"},
                connect_timeout=5,
                read_timeout=10,
                retries={"max_attempts": 2, "mode": "standard"},
            ),
        )

    @staticmethod
    def _object_key(file_url: str) -> str:
        """T10 stores object keys in file_url, not public playback URLs."""
        if not isinstance(file_url, str) or not file_url.strip():
            raise ValueError("file_url must contain an S3 object key")

        key = file_url.strip()
        if key.startswith("/") or "://" in key:
            raise ValueError(
                "file_url must be an object key, not an absolute URL"
            )

        return key

    async def get_access_url(self, file_url: str) -> Optional[str]:
        key = self._object_key(file_url)

        # boto3 is synchronous; do not block FastAPI's event loop.
        return await asyncio.to_thread(
            self._client.generate_presigned_url,
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=self.presigned_url_expires_in,
        )

    async def inspect(
        self,
        file_url: str,
    ) -> Optional[StorageObjectMetadata]:
        key = self._object_key(file_url)

        try:
            response = await asyncio.to_thread(
                self._client.head_object,
                Bucket=self.bucket,
                Key=key,
            )
        except ClientError as error:
            error_code = str(
                error.response.get("Error", {}).get("Code", "")
            )
            status_code = error.response.get(
                "ResponseMetadata", {}
            ).get("HTTPStatusCode")

            if status_code == 404 or error_code in {
                "404",
                "NoSuchKey",
                "NotFound",
            }:
                return None

            raise

        object_metadata = {
            str(name).lower(): str(value)
            for name, value in response.get("Metadata", {}).items()
        }

        # Use explicit metadata, rather than assuming ETag is SHA-256.
        checksum = (
            object_metadata.get("checksum")
            or object_metadata.get("sha256")
        )

        size = response.get("ContentLength")

        return StorageObjectMetadata(
            size=int(size) if size is not None else None,
            checksum=checksum,
        )

    async def read(self, file_url: str) -> Optional[tuple[bytes, str]]:
        key = self._object_key(file_url)

        def _read_object():
            response = self._client.get_object(Bucket=self.bucket, Key=key)
            body = response["Body"]
            try:
                return body.read(), response.get("ContentType", "audio/mpeg")
            finally:
                body.close()

        try:
            return await asyncio.to_thread(_read_object)
        except ClientError as error:
            code = str(error.response.get("Error", {}).get("Code", ""))
            if code in {"404", "NoSuchKey", "NotFound"}:
                return None
            raise

    async def put(self, file_url: str, content: bytes, media_type: str, checksum: str) -> None:
        key = self._object_key(file_url)
        await asyncio.to_thread(
            self._client.put_object, Bucket=self.bucket, Key=key, Body=content,
            ContentType=media_type, Metadata={"sha256": checksum},
        )
