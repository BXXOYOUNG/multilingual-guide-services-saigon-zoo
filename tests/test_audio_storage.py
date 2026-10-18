import asyncio

import pytest
from botocore.exceptions import ClientError

from backend.services import audio_storage
from backend.services.audio_storage import (
    S3CompatibleAudioStorageProvider,
    StorageObjectMetadata,
)


class FakeS3Client:
    """A minimal S3 client fake for isolated unit tests."""

    def __init__(self, head_response=None, head_error=None):
        self.head_response = head_response
        self.head_error = head_error
        self.head_object_call = None
        self.generated_url_call = None

    def generate_presigned_url(
        self,
        operation_name,
        *,
        Params,
        ExpiresIn,
    ):
        self.generated_url_call = {
            "operation_name": operation_name,
            "params": Params,
            "expires_in": ExpiresIn,
        }
        return "https://storage.example.test/presigned-audio"

    def head_object(self, **kwargs):
        self.head_object_call = kwargs

        if self.head_error is not None:
            raise self.head_error

        return self.head_response or {}


def make_provider(monkeypatch, fake_client, expires_in=300):
    """Construct the provider without opening a real S3 connection."""

    def fake_boto_client(service_name, **kwargs):
        assert service_name == "s3"
        assert kwargs["endpoint_url"] == "http://storage.example.test"
        assert kwargs["aws_access_key_id"] == "test-access-key"
        return fake_client

    monkeypatch.setattr(
        audio_storage.boto3,
        "client",
        fake_boto_client,
    )

    return S3CompatibleAudioStorageProvider(
        endpoint_url="http://storage.example.test",
        bucket="test-audio-bucket",
        access_key_id="test-access-key",
        secret_access_key="test-secret-key",
        region_name="us-east-1",
        presigned_url_expires_in=expires_in,
    )


def test_get_access_url_generates_presigned_url(monkeypatch):
    fake_client = FakeS3Client()
    provider = make_provider(monkeypatch, fake_client)

    result = asyncio.run(
        provider.get_access_url("animals/tiger.mp3")
    )

    assert result == "https://storage.example.test/presigned-audio"
    assert fake_client.generated_url_call == {
        "operation_name": "get_object",
        "params": {
            "Bucket": "test-audio-bucket",
            "Key": "animals/tiger.mp3",
        },
        "expires_in": 300,
    }


def test_inspect_reads_size_and_sha256_metadata(monkeypatch):
    checksum = "a" * 64
    fake_client = FakeS3Client(
        head_response={
            "ContentLength": 1234,
            "Metadata": {"sha256": checksum},
        }
    )
    provider = make_provider(monkeypatch, fake_client)

    result = asyncio.run(
        provider.inspect("animals/tiger.mp3")
    )

    assert result == StorageObjectMetadata(
        size=1234,
        checksum=checksum,
    )
    assert fake_client.head_object_call == {
        "Bucket": "test-audio-bucket",
        "Key": "animals/tiger.mp3",
    }


def test_inspect_reads_checksum_metadata_fallback(monkeypatch):
    checksum = "b" * 64
    fake_client = FakeS3Client(
        head_response={
            "ContentLength": 512,
            "Metadata": {"checksum": checksum},
        }
    )
    provider = make_provider(monkeypatch, fake_client)

    result = asyncio.run(
        provider.inspect("packages/audio.zip")
    )

    assert result == StorageObjectMetadata(
        size=512,
        checksum=checksum,
    )


def test_inspect_returns_none_when_object_is_missing(monkeypatch):
    error = ClientError(
        {
            "Error": {
                "Code": "NoSuchKey",
                "Message": "Object does not exist",
            },
            "ResponseMetadata": {"HTTPStatusCode": 404},
        },
        "HeadObject",
    )
    fake_client = FakeS3Client(head_error=error)
    provider = make_provider(monkeypatch, fake_client)

    result = asyncio.run(
        provider.inspect("animals/missing.mp3")
    )

    assert result is None


def test_inspect_propagates_non_not_found_storage_errors(monkeypatch):
    error = ClientError(
        {
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access denied",
            },
            "ResponseMetadata": {"HTTPStatusCode": 403},
        },
        "HeadObject",
    )
    fake_client = FakeS3Client(head_error=error)
    provider = make_provider(monkeypatch, fake_client)

    with pytest.raises(ClientError):
        asyncio.run(
            provider.inspect("animals/private.mp3")
        )


def test_access_url_rejects_absolute_url(monkeypatch):
    fake_client = FakeS3Client()
    provider = make_provider(monkeypatch, fake_client)

    with pytest.raises(ValueError, match="object key"):
        asyncio.run(
            provider.get_access_url(
                "https://example.com/animals/tiger.mp3"
            )
        )

    assert fake_client.generated_url_call is None


def test_provider_rejects_invalid_presigned_url_expiry(monkeypatch):
    fake_client = FakeS3Client()

    with pytest.raises(
        ValueError,
        match="between 1 and 604800",
    ):
        make_provider(
            monkeypatch,
            fake_client,
            expires_in=0,
        )
