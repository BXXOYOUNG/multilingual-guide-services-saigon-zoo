import unittest
from unittest import mock
from datetime import datetime
from bson import ObjectId
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.api.audio import get_audio_repository, router as audio_router
from backend.core.exception_handlers import register_exception_handlers
from backend.repositories.audio_repository import AudioRepository
from backend.schemas.audio import (
    AudioAssetResponse,
    AudioPackageResponse,
    AudioPackageManifest,
    AudioPackageStatus,
    AudioTaskResponse,
    AudioTaskStatus,
)


class FakeAsyncCursor:
    def __init__(self, documents):
        self._documents = iter(documents)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._documents)
        except StopIteration:
            raise StopAsyncIteration


class FakeCollection:
    def __init__(self, documents):
        self.documents = documents

    def find(self, query):
        matches = []
        for doc in self.documents:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                matches.append(doc)
        return FakeAsyncCursor(matches)

    async def find_one(self, query, sort=None):
        matches = []
        for doc in self.documents:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                matches.append(doc)
        if not matches:
            return None
        if sort:
            # Sort by field
            sort_field, sort_dir = sort[0]
            matches.sort(key=lambda d: d.get(sort_field, 0), reverse=(sort_dir == -1))
        return matches[0]


class FakeDatabase:
    def __init__(self, assets=None, packages=None, tasks=None):
        self.collections = {
            "audio_assets": FakeCollection(assets or []),
            "audio_packages": FakeCollection(packages or []),
            "audio_tasks": FakeCollection(tasks or []),
        }

    def __getitem__(self, name):
        return self.collections[name]


class AudioRepositoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_get_asset_by_poi_and_language(self):
        asset_id = ObjectId()
        poi_id = ObjectId()
        db = FakeDatabase(
            assets=[
                {
                    "_id": asset_id,
                    "poi_id": poi_id,
                    "language_code": "vi",
                    "file_path": "audio/vi/poi1.mp3",
                    "audio_url": "https://storage.example.com/audio/vi/poi1.mp3",
                    "duration_seconds": 45.5,
                    "file_size_bytes": 102400,
                    "format": "mp3",
                    "checksum": "abc123hash",
                }
            ]
        )
        repo = AudioRepository(db)

        asset = await repo.get_asset_by_poi_and_language(str(poi_id), "vi")
        self.assertIsNotNone(asset)
        self.assertEqual(asset.id, str(asset_id))
        self.assertEqual(asset.poi_id, str(poi_id))
        self.assertEqual(asset.audio_url, "https://storage.example.com/audio/vi/poi1.mp3")
        self.assertEqual(asset.duration_seconds, 45.5)

    async def test_get_package_manifest_with_assets(self):
        pkg_id = ObjectId()
        asset_id1 = ObjectId()
        asset_id2 = ObjectId()
        db = FakeDatabase(
            packages=[
                {
                    "_id": pkg_id,
                    "package_name": "Gói Tiếng Việt",
                    "language_code": "vi",
                    "version": "1.0.0",
                    "status": "ready",
                    "total_assets": 2,
                    "total_size_bytes": 204800,
                    "download_url": "https://storage.example.com/packages/pkg_vi.zip",
                    "checksum": "pkg123hash",
                }
            ],
            assets=[
                {
                    "_id": asset_id1,
                    "poi_id": ObjectId(),
                    "package_id": pkg_id,
                    "language_code": "vi",
                    "file_path": "audio/vi/1.mp3",
                    "audio_url": "https://storage.example.com/1.mp3",
                    "duration_seconds": 30.0,
                    "file_size_bytes": 102400,
                },
                {
                    "_id": asset_id2,
                    "poi_id": ObjectId(),
                    "package_id": pkg_id,
                    "language_code": "vi",
                    "file_path": "audio/vi/2.mp3",
                    "audio_url": "https://storage.example.com/2.mp3",
                    "duration_seconds": 35.0,
                    "file_size_bytes": 102400,
                },
            ],
        )
        repo = AudioRepository(db)

        manifest = await repo.get_package_manifest(str(pkg_id))
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.package_id, str(pkg_id))
        self.assertEqual(manifest.status, AudioPackageStatus.READY)
        self.assertEqual(len(manifest.assets), 2)
        self.assertEqual(manifest.total_assets, 2)


class AudioAPITests(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        register_exception_handlers(self.app)
        self.app.include_router(audio_router)
        self.repository = unittest.mock.Mock(spec=AudioRepository)
        self.app.dependency_overrides[get_audio_repository] = lambda: self.repository
        self.client = TestClient(self.app, raise_server_exceptions=False)

    def tearDown(self):
        self.client.close()

    def test_get_asset_by_poi_success(self):
        self.repository.get_asset_by_poi_and_language.return_value = AudioAssetResponse(
            id="asset-1",
            poi_id="poi-1",
            language_code="vi",
            file_path="audio/vi/poi1.mp3",
            audio_url="https://example.com/audio.mp3",
            duration_seconds=45.0,
            file_size_bytes=1024,
            format="mp3",
            checksum="hash1",
        )

        response = self.client.get("/api/audio/assets?poi_id=poi-1&language=vi")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "asset-1")
        self.assertEqual(data["audio_url"], "https://example.com/audio.mp3")

    def test_get_asset_by_poi_not_found(self):
        self.repository.get_asset_by_poi_and_language.return_value = None

        response = self.client.get("/api/audio/assets?poi_id=poi-unknown&language=vi")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "NOT_FOUND")

    def test_get_ready_package_by_language_success(self):
        self.repository.get_ready_package_by_language.return_value = AudioPackageResponse(
            id="pkg-vi",
            package_name="Gói Tiếng Việt",
            language_code="vi",
            version="1.0.0",
            status=AudioPackageStatus.READY,
            total_assets=10,
            total_size_bytes=5000000,
            download_url="https://example.com/pkg_vi.zip",
        )

        response = self.client.get("/api/audio/packages?language=vi")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "pkg-vi")
        self.assertEqual(data["status"], "ready")

    def test_get_package_manifest_success(self):
        self.repository.get_package_manifest.return_value = AudioPackageManifest(
            package_id="pkg-vi",
            package_name="Gói Tiếng Việt",
            language_code="vi",
            version="1.0.0",
            status=AudioPackageStatus.READY,
            total_assets=1,
            total_size_bytes=1024,
            assets=[
                AudioAssetResponse(
                    id="asset-1",
                    poi_id="poi-1",
                    language_code="vi",
                    file_path="1.mp3",
                    audio_url="https://example.com/1.mp3",
                    duration_seconds=10.0,
                    file_size_bytes=1024,
                )
            ],
        )

        response = self.client.get("/api/audio/packages/pkg-vi/manifest")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["package_id"], "pkg-vi")
        self.assertEqual(len(data["assets"]), 1)

    def test_get_task_status(self):
        self.repository.get_task_by_id.return_value = AudioTaskResponse(
            id="task-1",
            poi_id="poi-1",
            language_code="vi",
            status=AudioTaskStatus.COMPLETED,
        )

        response = self.client.get("/api/audio/tasks/task-1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "completed")


if __name__ == "__main__":
    unittest.main()

