import unittest

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from backend.core.exception_handlers import register_exception_handlers

from backend.main import app as main_app


class APIErrorHandlerTests(unittest.TestCase):
    def setUp(self):
        app = FastAPI()
        register_exception_handlers(app)

        @app.get("/items")
        def get_items(limit: int):
            return {"limit": limit}

        @app.get("/missing")
        def get_missing_resource():
            raise HTTPException(
                status_code=404,
                detail="Resource not found",
            )

        @app.get("/boom")
        def trigger_unexpected_error():
            raise RuntimeError("internal secret detail")

        self.client = TestClient(
            app,
            raise_server_exceptions=False,
        )

    def tearDown(self):
        self.client.close()

    def test_validation_error_uses_standard_response(self):
        response = self.client.get("/items?limit=invalid")

        self.assertEqual(response.status_code, 422)

        error = response.json()["error"]
        self.assertEqual(error["code"], "VALIDATION_ERROR")
        self.assertEqual(
            error["message"],
            "Request validation failed",
        )
        self.assertEqual(error["details"][0]["location"], ["query", "limit"])
        self.assertIn("type", error["details"][0])
        self.assertNotIn("input", error["details"][0])

    def test_http_error_preserves_status_and_standardizes_body(self):
        response = self.client.get("/missing")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                "error": {
                    "code": "NOT_FOUND",
                    "message": "Resource not found",
                    "details": [],
                }
            },
        )

    def test_unexpected_error_does_not_leak_internal_detail(self):
        response = self.client.get("/boom")

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
        self.assertNotIn("internal secret detail", response.text)

class MainApplicationIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(
            main_app,
            raise_server_exceptions=False,
        )

    def tearDown(self):
        self.client.close()

    def test_health_response_remains_unchanged(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "healthy"},
        )

    def test_unknown_route_uses_standard_error_response(self):
        response = self.client.get("/route-that-does-not-exist")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                "error": {
                    "code": "NOT_FOUND",
                    "message": "Not Found",
                    "details": [],
                }
            },
        )

if __name__ == "__main__":
    unittest.main()