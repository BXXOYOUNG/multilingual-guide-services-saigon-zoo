
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

## 7. POI Read API

`GET /api/pois?language=<language-code>` returns an unwrapped JSON array. The
language query parameter is required. Only active POIs with an exact-language
localization are returned; no fallback language is selected. Results are not
paginated, filtered, or sorted by request parameters.

Each POI has this response shape:

```json
{
  "id": "MongoDB ObjectId as a string",
  "name": "Localized POI name",
  "description": "Localized POI description",
  "latitude": 10.78,
  "longitude": 106.7
}
```

The backend reads from the existing `poi` and `poi_localizations` collections,
associating localization records through `poi_localizations.poi_id`. It does
not create or update POI data.

## 8. Admin content workflow (2026-11-04)

All writes below require the existing HTTP-only admin cookie and permission checks.
IDs on the wire are 24-character ObjectId strings; stored references remain BSON ObjectId.

| Endpoint | Permission | Contract |
|---|---|---|
| `POST /api/admin/pois` | `poi:write`, plus `content:write` when initial localization is supplied | Optional `initial_localization: {language_code,title,description}`; default hidden; returns 201 `{id}` |
| `POST /api/admin/pois/{id}/image` | `poi:write` | Raw JPEG/PNG/WebP body, max 5 MB/16 MP; returns `{image_url}` |
| `GET /api/media/pois/{id}/{sha256.ext}` | Public | Validated uploaded image; immutable cache, nosniff |
| `PUT /api/admin/pois/{id}/geofence` | `poi:write` | `{radius:5..500,is_active:boolean}`, center from saved POI |
| `GET /api/admin/audio-voices` | `audio:write` | Map of language code to supported voice IDs |
| `POST /api/admin/pois/{id}/localizations/{language}/generate-audio` | `audio:write` | `{voice:null or supported ID}`, saved text required; 202 `{id,status}`; duplicate active job 409 |
| `GET /api/admin/audio-jobs/{id}` | `audio:write` | `{id,status,error_message,voice}`; status Pending/Processing/Completed/Failed |
| `POST /api/admin/audio-packages` | `audio:write` | `{name,language_code}`; creates immutable audio snapshot from active POIs; 201 `{id,name,asset_count}`; invalid/missing audio 409 |
| `GET /audio/packages` | Public | Nonempty offline packages, newest first; `{id,name,language_code,asset_count}[]` |

Generation uses in-process FastAPI BackgroundTasks with a 5-minute Redis lease, not a durable job queue. Audio is published to the current localization only if task ID and source text/title still match. Jobs interrupted by a restart become Failed when queried after five minutes. New snapshot package/asset membership cannot be reassigned through the legacy assignment API. Existing legacy packages remain readable.

## 9. Admin translation (2026-11-09)

All three endpoints require the existing cookie and `content:write`. Supported source/targets: `vi`, `en`, `fr`, `zh-Hans`, `ja`, `ko`. Automatic translation requires backend `GOOGLE_TRANSLATE_API_KEY`; manual localization PUT remains supported without a key. The adapter maps `zh-Hans` to provider code `zh-CN` only on outbound calls.

| Endpoint | Request | Response |
|---|---|---|
| `GET /api/admin/translation-settings` | None | `{configured:boolean,provider,languages,preview_ttl_seconds:1800}`; configured indicates key presence, not validity |
| `POST /api/admin/pois/{id}/translations/preview` | `{source_language,title,description,targets:[code,...]}`; 1–5 unique targets, excluding source; source must exactly match saved localization | `{preview_id,expires_in:1800,provider,results:[...]}` |
| `POST /api/admin/pois/{id}/translations/commit` | `{preview_id,items:[{language_code,title,description,replace_existing:false}]}`; 1–5 unique successful targets from this preview | `{saved:[code,...],audio_generation_required:true}`; reminder to generate audio where needed, not evidence every unchanged target requires regeneration |

Limits: title 1–180 characters, description 1–10000, neither whitespace-only. Preview targets are explicit; current UI requests the other five languages, then retries failed targets. One provider batch per admin/30 seconds (429 otherwise). Each provider request includes source title/description as plain text; no automatic paid retries.

Successful preview row: `{language_code,title,description,existing,existing_title,existing_description,revision}`. A failed row has `{language_code,error}`. HTTP 200 can contain partial or all provider failures; no localization is saved by preview. Missing backend key returns 503 through the standard sanitized server-error envelope; the settings endpoint lets UI explain configuration beforehand. Wrong POI 404; unsupported/duplicate languages or invalid fields 422; unsaved/mismatched source 409.

Preview drafts are private Redis records bound to admin/POI for 1800 seconds. Commit accepts edited title/description but only languages successfully translated in that preview. Existing targets require `replace_existing:true`. Expired previews, changed source/target revisions, missing replacement confirmation or transaction failure return 409. Accessing another admin/POI preview returns 403. Provider errors and responses never expose API keys.

Commit checks/creates a unique `(poi_id,language_code)` index, refusing duplicates without deleting records. It requires the existing MongoDB replica set. A source write guard and target revision checks protect concurrent edits; selected targets from one preview commit in one transaction. Different preview groups after retries are separate transactions: earlier successful groups stay saved if a later group fails. If a network error leaves commit outcome unknown, reload before retrying. Replaying a saved preview is rejected by changed revisions.

Saved translations include optional provenance/review metadata. Editing source marks dependent translations `needs_review`; unchanged target audio is retained until that target text changes. Changed target title/description invalidates current audio/task pointers. TTS and package publishing remain separate explicit actions. Saved localization text of active POIs is immediately readable; only preview drafts are kept outside public content. See [ADMIN_AUTO_TRANSLATION.md](ADMIN_AUTO_TRANSLATION.md).

`GET /api/admin/pois?language=...` also returns optional `translation_review_status` (`null`, `needs_review`, `edited_by_admin`, `reviewed_by_admin`) for the selected localization. Explicit manual saving acknowledges review; changing source content can mark it for review again.
