
# API Conventions

## 1. Scope

The backend exposes REST APIs using FastAPI. API contracts must remain consistent
across modules without changing the approved architecture.

This document defines the current conventions for successful responses,
validation errors, HTTP errors, and unexpected server errors.

## 2. Successful Responses

- Return the response structure appropriate to the endpoint.
- Do not wrap every successful response in a global `data` envelope.
- Use Pydantic `response_model` when a response schema has been defined.
- Use appropriate HTTP status codes.
- Preserve existing endpoint behavior unless a task explicitly requires a change.

The `/health` endpoint currently returns:

```json
{
  "status": "healthy"
}
```

## 3. Standard Error Response

All errors handled by the shared exception handlers use this structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "location": ["query", "limit"],
        "message": "Input should be a valid integer",
        "type": "int_parsing"
      }
    ]
  }
}
```

Fields:

- `error.code`: stable machine-readable error identifier.
- `error.message`: human-readable message safe to return to the client.
- `error.details`: an array of additional error details; an empty array is used when no details are available.
- `details[].location`: input location, represented as an array of strings or integers.
- `details[].message`: description of the specific validation issue.
- `details[].type`: validation error type when available.

## 4. Error Mapping

### 4.1. Request validation

Invalid request data returns HTTP `422` with:

- Code: `VALIDATION_ERROR`
- Message: `Request validation failed`
- Details: location, message, and type for each validation error.

Only the selected validation fields are returned. Raw input values and internal exception context are not included in the response.

### 4.2. HTTP exceptions

The following mappings are defined:

| HTTP status | Error code |
|---|---|
| 400 | `BAD_REQUEST` |
| 401 | `UNAUTHORIZED` |
| 403 | `FORBIDDEN` |
| 404 | `NOT_FOUND` |
| 405 | `METHOD_NOT_ALLOWED` |
| 409 | `CONFLICT` |
| 413 | `PAYLOAD_TOO_LARGE` |
| 415 | `UNSUPPORTED_MEDIA_TYPE` |
| 429 | `TOO_MANY_REQUESTS` |

Other HTTP errors below `500` use `HTTP_ERROR` unless an explicit mapping is added.

For HTTP exceptions with a status of `500` or higher, use the
`INTERNAL_SERVER_ERROR` code and a generic client-facing message.

HTTP exception details returned to clients must be safe and must not contain
credentials, stack traces, database diagnostics, or other internal information.

### 4.3. Unexpected exceptions

Unexpected exceptions return HTTP `500` with:

```json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred",
    "details": []
  }
}
```

The server logs the exception and traceback for diagnostics.
Internal exception details must not be exposed in the response.

## 5. Implementation

- Shared error schemas live in `backend/schemas/common.py`.
- Shared exception handlers live in `backend/core/exception_handlers.py`.
- `register_exception_handlers(app)` must be called when initializing the FastAPI application.
- New endpoint modules must reuse the shared conventions rather than define competing error formats.
- Business modules must not implement separate global exception handlers.

## 6. Verification

Run the backend tests with:

```powershell
python -m unittest discover -s tests -v
```

Check the working diff with:

```powershell
git diff --check
```
