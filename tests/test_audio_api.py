import unittest
import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any

from bson import ObjectId
from fastapi.testclient import TestClient

from backend.api.audio import get_audio_storage_provider
from backend.database.mongodb import get_database
from backend.main import app
from backend.schemas.audio import AudioAssetCreate
from backend.services.audio import AudioService
from backend.services.audio_storage import StorageObjectMetadata


class FakeCursor:
    def __init__(self, documents: list[dict[str, Any]]):
        self.documents = documents

    async def to_list(self, length: int | None = None) -> list[dict[str, Any]]:
        return list(self.documents if length is None else self.documents[:length])


class TransactionUnsupportedError(RuntimeError):
    code = 20


class UnrelatedCode20Error(RuntimeError):
    code = 20


class FakeTransaction:
    def __init__(self, owner):
        self.owner = owner

    async def __aenter__(self):
        self.owner.transaction_count += 1
        if self.owner.transaction_error is not None:
            raise self.owner.transaction_error

    async def __aexit__(self, exc_type, exc_value, traceback):
        return False


class FakeSession:
    def __init__(self, owner):
        self.owner = owner

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return False

    def start_transaction(self):
        return FakeTransaction(self.owner)


class FakeMongoClient:
    def __init__(self, transaction_error: Exception | None = None):
        self.transaction_error = transaction_error
        self.transaction_count = 0

    def start_session(self):
        return FakeSession(self)


class FakeCollection:
    def __init__(self):
        self.documents: list[dict[str, Any]] = []
        self.insert_error: Exception | None = None
        self.update_errors: list[Exception] = []
        self.update_applied_errors: list[tuple[Exception, Any]] = []
        self.update_before_match: list[Any] = []
        self.update_no_match_count = 0
        self.insert_count = 0

    async def insert_one(
        self,
        document: dict[str, Any],
        session: Any = None,
    ) -> SimpleNamespace:
        await asyncio.sleep(0)
        self.insert_count += 1
        if self.insert_error is not None:
            raise self.insert_error
        stored = dict(document)
        stored.setdefault("_id", ObjectId())
        self.documents.append(stored)
        return SimpleNamespace(inserted_id=stored["_id"])

    async def find_one(
        self,
        query: dict[str, Any],
        sort: list[tuple[str, int]] | None = None,
        session: Any = None,
    ) -> dict[str, Any] | None:
        await asyncio.sleep(0)
        matches = [item for item in self.documents if self._matches(item, query)]
        if sort:
            key, direction = sort[0]
            matches.sort(key=lambda item: item.get(key), reverse=direction < 0)
        return dict(matches[0]) if matches else None

    def find(self, query: dict[str, Any], session: Any = None) -> FakeCursor:
        return FakeCursor(
            [dict(item) for item in self.documents if self._matches(item, query)]
        )

    async def update_one(
        self,
        query: dict[str, Any],
        update: dict[str, Any],
        session: Any = None,
    ) -> SimpleNamespace:
        await asyncio.sleep(0)
        if self.update_errors:
            raise self.update_errors.pop(0)
        if self.update_no_match_count:
            self.update_no_match_count -= 1
            for index, item in enumerate(self.documents):
                if self._matches(item, query):
                    del self.documents[index]
                    break
            return SimpleNamespace(matched_count=0)
        if self.update_before_match:
            self.update_before_match.pop(0)()
        for item in self.documents:
            if self._matches(item, query):
                item.update(update.get("$set", {}))
                for key in update.get("$unset", {}):
                    item.pop(key, None)
                if self.update_applied_errors:
                    error, callback = self.update_applied_errors.pop(0)
                    if callback is not None:
                        callback(item)
                    raise error
                return SimpleNamespace(matched_count=1)
        return SimpleNamespace(matched_count=0)

    @staticmethod
    def _matches(document: dict[str, Any], query: dict[str, Any]) -> bool:
        for key, value in query.items():
            if isinstance(value, dict) and "$exists" in value:
                if (key in document) != value["$exists"]:
                    return False
            elif key not in document or document[key] != value:
                return False
        return True


class FakeDatabase:
    def __init__(self):
        self.client = None
        self.collections = {
            name: FakeCollection()
            for name in (
                "audio_tasks",
                "audio_packages",
                "audio_assets",
                "poi_localizations",
            )
        }

    def __getitem__(self, name: str) -> FakeCollection:
        return self.collections[name]


class FakeStorageProvider:
    def __init__(
        self,
        metadata: dict[str, StorageObjectMetadata] | None = None,
    ):
        self.metadata = metadata or {}

    async def get_access_url(self, file_url: str) -> str:
        return f"https://storage.example.test/access/{file_url}"

    async def inspect(
        self,
        file_url: str,
    ) -> StorageObjectMetadata | None:
        return self.metadata.get(file_url)


class AudioAPITests(unittest.TestCase):
    def setUp(self):
        self.database = FakeDatabase()
        self.storage = None
        app.dependency_overrides[get_database] = lambda: self.database
        app.dependency_overrides[get_audio_storage_provider] = lambda: self.storage
        self.client = TestClient(app, raise_server_exceptions=False)
        self.poi_id = ObjectId()
        self.other_poi_id = ObjectId()
        self.package_id = ObjectId()
        self.now = datetime.now(timezone.utc)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()

    def add_localization(
        self,
        poi_id: ObjectId,
        language_code: str,
        audio_url: str | None = None,
    ) -> dict[str, Any]:
        document = {
            "_id": ObjectId(),
            "poi_id": poi_id,
            "language_code": language_code,
            "audio_url": audio_url,
        }
        self.database["poi_localizations"].documents.append(document)
        return document

    def add_package(
        self,
        package_id: ObjectId | None = None,
        language_code: str = "en",
        file_url: str = "packages/en.zip",
        file_size: int = 1024,
    ) -> dict[str, Any]:
        package = {
            "_id": package_id or ObjectId(),
            "name": "English audio",
            "language_code": language_code,
            "description": "English offline audio",
            "file_url": file_url,
            "file_size": file_size,
            "is_offline": True,
            "created_at": self.now,
        }
        self.database["audio_packages"].documents.append(package)
        return package

    def add_asset(
        self,
        package_id: ObjectId | None,
        poi_id: ObjectId | None = None,
        language_code: str = "en",
        file_url: str = "audio/poi-one-en.mp3",
        checksum: str = "abc123",
    ) -> dict[str, Any]:
        asset = {
            "_id": ObjectId(),
            "package_id": package_id,
            "poi_id": poi_id or self.poi_id,
            "language_code": language_code,
            "file_url": file_url,
            "duration": 12.5,
            "checksum": checksum,
            "created_at": self.now,
        }
        self.database["audio_assets"].documents.append(asset)
        return asset

    @staticmethod
    def assert_standard_error(
        test: unittest.TestCase,
        response,
        status_code: int,
        error_code: str,
    ) -> None:
        test.assertEqual(response.status_code, status_code)
        test.assertEqual(
            set(response.json()),
            {"error"},
        )
        test.assertEqual(response.json()["error"]["code"], error_code)
        test.assertIsInstance(response.json()["error"]["details"], list)

    def test_object_ids_are_validated_in_requests_and_paths(self):
        invalid_body = self.client.post(
            "/audio/tasks",
            json={
                "poi_id": "not-an-object-id",
                "language_code": "en",
                "type": "TTS",
            },
        )
        self.assert_standard_error(self, invalid_body, 422, "VALIDATION_ERROR")

        invalid_path = self.client.get("/audio/tasks/not-an-object-id")
        self.assert_standard_error(self, invalid_path, 400, "BAD_REQUEST")

        response = self.client.post(
            "/audio/tasks",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "type": "TTS",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["poi_id"], str(self.poi_id))

    def test_task_state_transitions_do_not_create_playable_audio(self):
        localization = self.add_localization(self.poi_id, "en")
        created = self.client.post(
            "/audio/tasks",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "type": "Manual",
            },
        )
        task_id = created.json()["_id"]
        self.assertEqual(created.json()["status"], "Pending")
        self.assertIsNone(created.json()["file_url"])

        invalid_transition = self.client.patch(
            f"/audio/tasks/{task_id}/status",
            json={"status": "Completed", "file_url": "task/result.mp3"},
        )
        self.assert_standard_error(self, invalid_transition, 409, "CONFLICT")

        self.assertEqual(localization["audio_url"], None)
        self.assert_standard_error(
            self,
            self.client.get(
                f"/audio/assets/resolve?poi_id={self.poi_id}&language_code=en"
            ),
            404,
            "NOT_FOUND",
        )

        processing = self.client.patch(
            f"/audio/tasks/{task_id}/status",
            json={"status": "Processing"},
        )
        self.assertEqual(processing.json()["status"], "Processing")
        completed = self.client.patch(
            f"/audio/tasks/{task_id}/status",
            json={"status": "Completed", "file_url": "task/result.mp3"},
        )
        self.assertEqual(completed.json()["file_url"], "task/result.mp3")
        self.assertIsNone(localization["audio_url"])
        self.assert_standard_error(
            self,
            self.client.get(
                f"/audio/assets/resolve?poi_id={self.poi_id}&language_code=en"
            ),
            404,
            "NOT_FOUND",
        )

    def test_all_allowed_and_forbidden_task_transitions(self):
        allowed = {
            "Pending": ("Processing", "Failed"),
            "Processing": ("Completed", "Failed"),
        }
        for current_status, next_statuses in allowed.items():
            for next_status in next_statuses:
                with self.subTest(current=current_status, next=next_status):
                    task_id = ObjectId()
                    self.database["audio_tasks"].documents.append(
                        {
                            "_id": task_id,
                            "poi_id": self.poi_id,
                            "language_code": "en",
                            "type": "TTS",
                            "status": current_status,
                            "file_url": None,
                            "created_at": self.now,
                            "updated_at": self.now,
                        }
                    )
                    response = self.client.patch(
                        f"/audio/tasks/{task_id}/status",
                        json={"status": next_status},
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json()["status"], next_status)

        forbidden = {
            "Pending": ("Completed",),
            "Processing": ("Pending",),
            "Completed": ("Pending", "Processing", "Failed"),
            "Failed": ("Pending", "Processing", "Completed"),
        }
        for current_status, next_statuses in forbidden.items():
            for next_status in next_statuses:
                with self.subTest(current=current_status, next=next_status):
                    task_id = ObjectId()
                    self.database["audio_tasks"].documents.append(
                        {
                            "_id": task_id,
                            "poi_id": self.poi_id,
                            "language_code": "en",
                            "type": "TTS",
                            "status": current_status,
                            "file_url": None,
                            "created_at": self.now,
                            "updated_at": self.now,
                        }
                    )
                    response = self.client.patch(
                        f"/audio/tasks/{task_id}/status",
                        json={"status": next_status},
                    )
                    self.assert_standard_error(self, response, 409, "CONFLICT")

        invalid_request = self.client.patch(
            f"/audio/tasks/{ObjectId()}/status",
            json={"status": "Ready"},
        )
        self.assert_standard_error(self, invalid_request, 422, "VALIDATION_ERROR")

        corrupt_task_id = ObjectId()
        self.database["audio_tasks"].documents.append(
            {
                "_id": corrupt_task_id,
                "poi_id": self.poi_id,
                "language_code": "en",
                "type": "TTS",
                "status": "Corrupt",
                "file_url": None,
                "created_at": self.now,
                "updated_at": self.now,
            }
        )
        invalid_stored_status = self.client.patch(
            f"/audio/tasks/{corrupt_task_id}/status",
            json={"status": "Failed"},
        )
        self.assert_standard_error(
            self,
            invalid_stored_status,
            409,
            "CONFLICT",
        )
        self.assertEqual(
            self.database["audio_tasks"].documents[-1]["status"],
            "Corrupt",
        )
        invalid_stored_status_get = self.client.get(
            f"/audio/tasks/{corrupt_task_id}"
        )
        self.assert_standard_error(
            self,
            invalid_stored_status_get,
            409,
            "CONFLICT",
        )

    def test_ready_audio_requires_exact_poi_and_language_and_updates_localization(self):
        english = self.add_localization(self.poi_id, "en")
        vietnamese = self.add_localization(self.poi_id, "vi", "old/vi.mp3")
        other_poi_english = self.add_localization(self.other_poi_id, "en")
        self.add_asset(None, self.poi_id, "vi", "audio/vi.mp3")

        response = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/en.mp3",
                "duration": 15,
                "checksum": "sha256:abcdef",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["playback_url"], None)
        self.assertEqual(english["audio_url"], "audio/en.mp3")
        self.assertEqual(vietnamese["audio_url"], "old/vi.mp3")
        self.assertIsNone(other_poi_english["audio_url"])

        resolved = self.client.get(
            f"/audio/assets/resolve?poi_id={self.poi_id}&language_code=en"
        )
        self.assertEqual(resolved.status_code, 200)
        self.assertEqual(resolved.json()["file_url"], "audio/en.mp3")
        self.assertEqual(
            self.client.get(
                f"/audio/assets/resolve?poi_id={self.poi_id}&language_code=vi"
            ).json()["file_url"],
            "audio/vi.mp3",
        )

    def test_asset_requires_a_matching_existing_localization_and_package(self):
        mismatch = self.client.post(
            "/audio/assets",
            json={
                "package_id": str(ObjectId()),
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/en.mp3",
                "duration": 1,
                "checksum": "checksum",
            },
        )
        self.assert_standard_error(self, mismatch, 404, "NOT_FOUND")

        self.add_package(language_code="vi")
        self.add_localization(self.poi_id, "en")
        wrong_language = self.client.post(
            "/audio/assets",
            json={
                "package_id": str(self.database["audio_packages"].documents[0]["_id"]),
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/en.mp3",
                "duration": 1,
                "checksum": "checksum",
            },
        )
        self.assert_standard_error(self, wrong_language, 409, "CONFLICT")

    def test_asset_registration_requires_the_exact_localization(self):
        request = {
            "poi_id": str(self.poi_id),
            "language_code": "en",
            "file_url": "audio/missing-localization.mp3",
            "duration": 1,
            "checksum": "missing-localization",
        }
        response = self.client.post("/audio/assets", json=request)
        self.assert_standard_error(self, response, 404, "NOT_FOUND")
        self.assertEqual(self.database["audio_assets"].documents, [])

        english = self.add_localization(self.poi_id, "en")
        vietnamese = self.add_localization(self.poi_id, "vi", "old/vi.mp3")
        other_poi = self.add_localization(self.other_poi_id, "en")
        response = self.client.post("/audio/assets", json=request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(english["audio_url"], request["file_url"])
        self.assertEqual(vietnamese["audio_url"], "old/vi.mp3")
        self.assertIsNone(other_poi["audio_url"])

    def test_asset_registration_insert_failure_does_not_update_localization(self):
        localization = self.add_localization(self.poi_id, "en", "old.mp3")
        self.database["audio_assets"].insert_error = RuntimeError("insert failed")

        response = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/new.mp3",
                "duration": 1,
                "checksum": "insert-failure",
            },
        )
        self.assert_standard_error(
            self,
            response,
            500,
            "INTERNAL_SERVER_ERROR",
        )
        self.assertEqual(self.database["audio_assets"].documents, [])
        self.assertEqual(localization["audio_url"], "old.mp3")

    def test_asset_registration_localization_exception_is_retained_for_retry(self):
        localization = self.add_localization(self.poi_id, "en", "old.mp3")
        self.database["poi_localizations"].update_errors.append(
            RuntimeError("localization update failed")
        )

        response = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/new.mp3",
                "duration": 1,
                "checksum": "localization-error",
            },
        )
        self.assert_standard_error(
            self,
            response,
            500,
            "INTERNAL_SERVER_ERROR",
        )
        self.assertEqual(len(self.database["audio_assets"].documents), 1)
        self.assertEqual(localization["audio_url"], "old.mp3")

    def test_asset_registration_retains_asset_if_localization_disappears(self):
        self.add_localization(self.poi_id, "en")
        self.database["poi_localizations"].update_no_match_count = 1

        response = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/no-match.mp3",
                "duration": 1,
                "checksum": "no-match",
            },
        )
        self.assert_standard_error(self, response, 404, "NOT_FOUND")
        self.assertEqual(len(self.database["audio_assets"].documents), 1)
        self.assertEqual(self.database["poi_localizations"].documents, [])

    def test_same_url_written_before_update_error_is_never_rolled_back(self):
        target_url = "audio/same-url.mp3"
        self.add_localization(self.poi_id, "en", "audio/old.mp3")
        self.database["poi_localizations"].update_applied_errors.append(
            (
                RuntimeError("connection lost after write"),
                lambda localization: localization.update(
                    {"audio_url": target_url}
                ),
            )
        )
        response = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": target_url,
                "duration": 1,
                "checksum": "same-url-race",
            },
        )
        self.assert_standard_error(
            self,
            response,
            500,
            "INTERNAL_SERVER_ERROR",
        )
        self.assertEqual(
            self.database["poi_localizations"].documents[0]["audio_url"],
            target_url,
        )
        self.assertEqual(len(self.database["audio_assets"].documents), 1)
        retried = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": target_url,
                "duration": 1,
                "checksum": "same-url-race",
            },
        )
        self.assertEqual(retried.status_code, 201)
        self.assertEqual(len(self.database["audio_assets"].documents), 1)

    def test_concurrent_different_url_is_not_overwritten_by_registration(self):
        localization = self.add_localization(self.poi_id, "en", "audio/old.mp3")
        localization_collection = self.database["poi_localizations"]
        localization_collection.update_before_match.append(
            lambda: localization.update({"audio_url": "audio/concurrent.mp3"})
        )
        response = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/registration.mp3",
                "duration": 1,
                "checksum": "different-url-race",
            },
        )
        self.assert_standard_error(self, response, 409, "CONFLICT")
        self.assertEqual(localization["audio_url"], "audio/concurrent.mp3")
        self.assertEqual(len(self.database["audio_assets"].documents), 1)

    def test_identical_asset_registration_is_idempotent_and_conflicts_on_metadata(self):
        self.add_localization(self.poi_id, "en")
        request = {
            "poi_id": str(self.poi_id),
            "language_code": "en",
            "file_url": "audio/deduplicated.mp3",
            "duration": 2,
            "checksum": "duplicate-checksum",
        }
        first = self.client.post("/audio/assets", json=request)
        second = self.client.post("/audio/assets", json=request)
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(first.json()["_id"], second.json()["_id"])
        self.assertEqual(len(self.database["audio_assets"].documents), 1)

        conflicting = self.client.post(
            "/audio/assets",
            json={**request, "file_url": "audio/different.mp3"},
        )
        self.assert_standard_error(self, conflicting, 409, "CONFLICT")
        self.assertEqual(len(self.database["audio_assets"].documents), 1)

    def test_duplicate_registration_does_not_overwrite_newer_audio_url(self):
        self.add_localization(self.poi_id, "en")

        request = {
            "poi_id": str(self.poi_id),
            "language_code": "en",
            "file_url": "audio/old.mp3",
            "duration": 2,
            "checksum": "retry-stale-checksum",
        }

        first = self.client.post("/audio/assets", json=request)
        self.assertEqual(first.status_code, 201)

        localization = self.database["poi_localizations"].documents[0]
        localization["audio_url"] = "audio/newer.mp3"

        second = self.client.post("/audio/assets", json=request)

        self.assert_standard_error(self, second, 409, "CONFLICT")
        self.assertEqual(localization["audio_url"], "audio/newer.mp3")
        self.assertEqual(len(self.database["audio_assets"].documents), 1)

    def test_transactional_duplicate_registration_does_not_overwrite_newer_audio_url(self):
        self.add_localization(self.poi_id, "en")
        client = FakeMongoClient()
        self.database.client = client

        request = {
            "poi_id": str(self.poi_id),
            "language_code": "en",
            "file_url": "audio/old.mp3",
            "duration": 2,
            "checksum": "transaction-stale-checksum",
        }

        first = self.client.post("/audio/assets", json=request)
        self.assertEqual(first.status_code, 201)

        localization = self.database["poi_localizations"].documents[0]
        localization["audio_url"] = "audio/newer.mp3"

        second = self.client.post("/audio/assets", json=request)

        self.assert_standard_error(self, second, 409, "CONFLICT")
        self.assertEqual(localization["audio_url"], "audio/newer.mp3")
        self.assertEqual(len(self.database["audio_assets"].documents), 1)
        self.assertEqual(client.transaction_count, 2)

    def test_identical_asset_registration_is_idempotent_with_transactions(self):
        self.add_localization(self.poi_id, "en")
        client = FakeMongoClient()
        self.database.client = client

        request = {
            "poi_id": str(self.poi_id),
            "language_code": "en",
            "file_url": "audio/transaction-duplicate.mp3",
            "duration": 2,
            "checksum": "transaction-duplicate-checksum",
        }

        first = self.client.post("/audio/assets", json=request)
        second = self.client.post("/audio/assets", json=request)

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(first.json()["_id"], second.json()["_id"])
        self.assertEqual(client.transaction_count, 2)
        self.assertEqual(len(self.database["audio_assets"].documents), 1)
        self.assertEqual(
            self.database["poi_localizations"].documents[0]["audio_url"],
            request["file_url"],
        )

    def test_concurrent_identical_asset_registration_is_idempotent(self):
        self.add_localization(self.poi_id, "en")
        request = AudioAssetCreate(
            poi_id=str(self.poi_id),
            language_code="en",
            file_url="audio/concurrent.mp3",
            duration=2,
            checksum="concurrent-checksum",
        )
        service = AudioService(self.database)

        async def register_twice():
            return await asyncio.gather(
                service.create_asset(request),
                service.create_asset(request),
            )

        first, second = asyncio.run(register_twice())
        self.assertEqual(first.id, second.id)
        self.assertEqual(len(self.database["audio_assets"].documents), 1)

    def test_asset_registration_uses_transactions_when_client_supports_them(self):
        self.add_localization(self.poi_id, "en")
        client = FakeMongoClient()
        self.database.client = client
        response = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/transaction.mp3",
                "duration": 1,
                "checksum": "transaction-supported",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(client.transaction_count, 1)
        self.assertEqual(len(self.database["audio_assets"].documents), 1)

    def test_asset_registration_falls_back_when_transactions_are_unsupported(self):
        self.add_localization(self.poi_id, "en")
        client = FakeMongoClient(
            TransactionUnsupportedError(
                "Transaction numbers are only allowed on a replica set member "
                "or mongos"
            )
        )
        self.database.client = client
        response = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/fallback.mp3",
                "duration": 1,
                "checksum": "transactions-unsupported",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(client.transaction_count, 1)
        self.assertEqual(len(self.database["audio_assets"].documents), 1)
        self.assertEqual(
            self.database["poi_localizations"].documents[0]["audio_url"],
            "audio/fallback.mp3",
        )

    def test_code_20_unrelated_to_transaction_support_does_not_fallback(self):
        self.add_localization(self.poi_id, "en")
        client = FakeMongoClient(
            UnrelatedCode20Error("application constraint failure")
        )
        self.database.client = client
        response = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/no-fallback.mp3",
                "duration": 1,
                "checksum": "unrelated-code-20",
            },
        )
        self.assert_standard_error(
            self,
            response,
            500,
            "INTERNAL_SERVER_ERROR",
        )
        self.assertEqual(client.transaction_count, 1)
        self.assertEqual(self.database["audio_assets"].insert_count, 0)
        self.assertEqual(self.database["audio_assets"].documents, [])
        self.assertIsNone(
            self.database["poi_localizations"].documents[0]["audio_url"]
        )

    def test_manifest_contains_only_package_members_and_matching_language(self):
        self.add_localization(self.poi_id, "en")
        package = self.add_package(package_id=self.package_id)
        member = self.add_asset(self.package_id, file_url="member.mp3")
        self.add_asset(ObjectId(), file_url="other-package.mp3")

        response = self.client.get(
            f"/audio/packages/{self.package_id}/manifest"
        )
        self.assertEqual(response.status_code, 200)
        manifest = response.json()
        self.assertEqual(manifest["package"]["_id"], str(package["_id"]))
        self.assertEqual(
            [asset["_id"] for asset in manifest["assets"]],
            [str(member["_id"])],
        )
        self.assertEqual(manifest["integrity_status"], "unverified")
        self.assertIsNone(manifest["package"]["download_url"])

    def test_package_rejects_language_mismatch_and_missing_resources(self):
        package = self.add_package(package_id=self.package_id)
        self.add_asset(self.package_id, language_code="vi")
        mismatch = self.client.get(
            f"/audio/packages/{self.package_id}/manifest"
        )
        self.assert_standard_error(self, mismatch, 409, "CONFLICT")

        missing_package = self.client.get(
            f"/audio/packages/{ObjectId()}/manifest"
        )
        self.assert_standard_error(self, missing_package, 404, "NOT_FOUND")
        missing_asset = self.client.post(
            f"/audio/packages/{package['_id']}/assets/{ObjectId()}"
        )
        self.assert_standard_error(self, missing_asset, 404, "NOT_FOUND")

    def test_storage_provider_only_returns_provider_issued_urls(self):
        self.add_localization(self.poi_id, "en")
        self.storage = FakeStorageProvider()
        created = self.client.post(
            "/audio/assets",
            json={
                "poi_id": str(self.poi_id),
                "language_code": "en",
                "file_url": "audio/object.mp3",
                "duration": 1,
                "checksum": "checksum",
            },
        )
        self.assertEqual(
            created.json()["playback_url"],
            "https://storage.example.test/access/audio/object.mp3",
        )

    def test_package_integrity_checks_available_size_and_checksums(self):
        self.add_package(package_id=self.package_id, file_size=100)
        asset = self.add_asset(
            self.package_id,
            file_url="asset.mp3",
            checksum="expected",
        )
        self.storage = FakeStorageProvider(
            {
                "packages/en.zip": StorageObjectMetadata(size=100),
                "asset.mp3": StorageObjectMetadata(
                    size=20,
                    checksum=asset["checksum"],
                ),
            }
        )
        verified = self.client.get(
            f"/audio/packages/{self.package_id}/manifest"
        )
        self.assertEqual(verified.json()["integrity_status"], "verified")

        self.storage = FakeStorageProvider(
            {
                "packages/en.zip": StorageObjectMetadata(size=99),
                "asset.mp3": StorageObjectMetadata(checksum="wrong"),
            }
        )
        invalid = self.client.get(
            f"/audio/packages/{self.package_id}/manifest"
        )
        self.assertEqual(invalid.json()["integrity_status"], "invalid")
        self.assertEqual(len(invalid.json()["integrity_errors"]), 2)


if __name__ == "__main__":
    unittest.main()
