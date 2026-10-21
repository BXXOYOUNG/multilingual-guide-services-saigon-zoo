import unittest
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.api.pois import get_poi_repository, router
from backend.core.exception_handlers import register_exception_handlers
from backend.repositories.poi_repository import POIRepository
from backend.schemas.poi import POIResponse


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
        self.find_calls = []

    def find(self, query, projection):
        self.find_calls.append((query, projection))
        if "is_active" in query:
            matches = [
                document
                for document in self.documents
                if document.get("is_active") == query["is_active"]
            ]
            return FakeAsyncCursor(matches)
        requested_ids = query["poi_id"]["$in"]
        language_code = query["language_code"]
        matches = [
            document
            for document in self.documents
            if document["poi_id"] in requested_ids
            and document["language_code"] == language_code
        ]
        return FakeAsyncCursor(matches)


class FakeDatabase:
    def __init__(self, pois, localizations):
        self.collections = {
            "poi": FakeCollection(pois),
            "poi_localizations": FakeCollection(localizations),
        }

    def __getitem__(self, name):
        return self.collections[name]


class POIRepositoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_queries_active_pois_and_exact_language_and_serializes_id(self):
        poi_id = object()
        database = FakeDatabase(
            [
                {
                    "_id": poi_id,
                    "is_active": True,
                    "latitude": 10.78,
                    "longitude": 106.7,
                },
                {
                    "_id": object(),
                    "is_active": False,
                    "latitude": 0,
                    "longitude": 0,
                },
            ],
            [
                {
                    "poi_id": poi_id,
                    "language_code": "vi",
                    "title": "Cổng chính",
                    "description": "Lối vào chính",
                },
                {
                    "poi_id": poi_id,
                    "language_code": "en",
                    "title": "Main gate",
                    "description": "Main entrance",
                },
            ],
        )

        result = await POIRepository(database).list_for_language("vi")

        self.assertEqual(
            result,
            [
                POIResponse(
                    id=str(poi_id),
                    name="Cổng chính",
                    description="Lối vào chính",
                    latitude=10.78,
                    longitude=106.7,
                )
            ],
        )
        self.assertEqual(
            database["poi"].find_calls[0][0],
            {"is_active": True, "latitude": {"$type": "number"}, "longitude": {"$type": "number"}},
        )
        self.assertEqual(
            database["poi_localizations"].find_calls[0][0],
            {
                "poi_id": {"$in": [poi_id]},
                "language_code": "vi",
            },
        )
        self.assertEqual(
            database["poi_localizations"].find_calls[0][1],
            {
                "_id": 0,
                "poi_id": 1,
                "title": 1,
                "description": 1,
                "translation_review_status": 1,
            },
        )

    async def test_returns_empty_when_no_active_pois_or_matching_language(self):
        empty_database = FakeDatabase([], [])
        self.assertEqual(
            await POIRepository(empty_database).list_for_language("vi"),
            [],
        )

        poi_id = object()
        no_translation_database = FakeDatabase(
            [
                {
                    "_id": poi_id,
                    "is_active": True,
                    "latitude": 10.78,
                    "longitude": 106.7,
                    "image_url": None, "image_source_url": None, "source_url": None,
                    "coordinate_source_url": None, "coordinate_status": None,
                    "translation_review_status": None,
                }
            ],
            [],
        )
        self.assertEqual(
            await POIRepository(no_translation_database).list_for_language("vi"),
            [],
        )


class POIAPITests(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        register_exception_handlers(self.app)
        self.app.include_router(router)
        self.repository = unittest.mock.Mock(spec=POIRepository)
        self.app.dependency_overrides[get_poi_repository] = lambda: self.repository
        self.client = TestClient(
            self.app,
            raise_server_exceptions=False,
        )

    def tearDown(self):
        self.client.close()

    def test_returns_pois_using_the_response_schema(self):
        self.repository.list_for_language.return_value = [
            POIResponse(
                id="507f1f77bcf86cd799439011",
                name="Main gate",
                description="Main entrance",
                latitude=10.78,
                longitude=106.7,
            )
        ]

        response = self.client.get("/api/pois?language=en")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": "507f1f77bcf86cd799439011",
                    "name": "Main gate",
                    "description": "Main entrance",
                    "latitude": 10.78,
                    "longitude": 106.7,
                    "image_url": None, "image_source_url": None, "source_url": None,
                    "coordinate_source_url": None, "coordinate_status": None, "translation_review_status": None,
                }
            ],
        )
        self.repository.list_for_language.assert_called_once_with("en")

    def test_empty_result_is_an_empty_array(self):
        self.repository.list_for_language.return_value = []

        response = self.client.get("/api/pois?language=vi")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_language_is_required_and_uses_shared_validation_error(self):
        response = self.client.get("/api/pois")

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()["error"]["code"],
            "VALIDATION_ERROR",
        )

    def test_empty_language_uses_shared_validation_error(self):
        response = self.client.get("/api/pois?language=")

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()["error"]["code"],
            "VALIDATION_ERROR",
        )

    def test_uninitialized_database_uses_shared_safe_error_response(self):
        del self.app.dependency_overrides[get_poi_repository]
        with patch(
            "backend.api.pois.get_database",
            side_effect=RuntimeError("MongoDB is not configured"),
        ):
            response = self.client.get("/api/pois?language=vi")
        self.app.dependency_overrides[get_poi_repository] = (
            lambda: self.repository
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(),
            {
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "details": [],
                }
            },
        )
        self.assertNotIn("MongoDB is not configured", response.text)


if __name__ == "__main__":
    unittest.main()
