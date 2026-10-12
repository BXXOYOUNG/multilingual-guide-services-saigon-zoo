import unittest

from backend.schemas.common import (
    APIErrorBody,
    APIErrorDetail,
    APIErrorResponse,
)


class APIErrorSchemaTests(unittest.TestCase):
    def test_validation_error_serializes_consistently(self):
        response = APIErrorResponse(
            error=APIErrorBody(
                code="VALIDATION_ERROR",
                message="Request validation failed",
                details=[
                    APIErrorDetail(
                        location=["query", "limit"],
                        message="Input should be a valid integer",
                        type="int_parsing",
                    )
                ],
            )
        )

        self.assertEqual(
            response.model_dump(),
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": [
                        {
                            "location": ["query", "limit"],
                            "message": "Input should be a valid integer",
                            "type": "int_parsing",
                        }
                    ],
                }
            },
        )

    def test_details_default_to_empty_list(self):
        response = APIErrorResponse(
            error=APIErrorBody(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
            )
        )

        self.assertEqual(
            response.model_dump()["error"]["details"],
            [],
        )


if __name__ == "__main__":
    unittest.main()