# Developer Guide

## Classroom demo

The app is configured for a fully simulated classroom demo. See [DEMO_DATASET.md](DEMO_DATASET.md) for the 11 POIs, 6-language content, generated audio, geofences, image credits, and repeatable seed commands.

Start the local visitor app and temporary HTTPS URL for camera testing:

```powershell
.\scripts\start_demo.ps1
```

The launcher uses `saigon_zoo_tcv_dataset_dev`, Redis, and SeaweedFS from the running Docker containers. It writes the current phone URL and QR beneath `.demo-run/`. The temporary URL works only while the tunnel is running. Stop the app and tunnel with `scripts/stop_demo.ps1`; MongoDB, Redis, and SeaweedFS stay running.

Create a named admin account from the repository root. The script asks for username, email and a password of at least 12 characters; it does not generate or print your password:

```powershell
$env:MONGODB_URI = 'mongodb://127.0.0.1:27018/?replicaSet=rs0'
$env:MONGODB_DATABASE = 'saigon_zoo_tcv_dataset_dev'
.\.venv\Scripts\python.exe -m scripts.create_admin
```

Admin uses an HTTP-only cookie and Redis session. Use your individually provisioned account; do not put admin passwords into this document. In `/admin`, select a content language, inspect POIs and generated audio, create a QR code for a POI or offline package, or inspect analytics.

The admin workflow now supports image upload, circular geofence configuration, saved-text TTS with voice selection/job status/preview, and publication of immutable audio snapshots. Follow [ADMIN_POI_WORKFLOW.md](ADMIN_POI_WORKFLOW.md). TTS runs in the API process and needs Internet; Redis supplies a per-POI/language lease, not a durable worker queue. Install updated `backend/requirements.txt` before restarting an older checkout.

## Local development

Backend dependencies and API (set MongoDB, Redis and S3 process environment first as shown in the handoff guide):

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
npm run build
```

The `GET /health` endpoint checks that the API process is running. The `GET /api/pois?language=<language-code>` route returns active POIs with an exact-language localization. The current frontend expects same-origin `/api` and `/audio` proxies. `VITE_API_BASE_URL` is only implemented by the POI repository, so it does not configure the whole app for a separate API origin.

## Configuration

The backend reads configuration from its process environment:

- `MONGODB_URI` and `MONGODB_DATABASE` configure MongoDB and must be set together.
- `REDIS_URL` configures Redis.
- `AUDIO_STORAGE_ENDPOINT_URL`, `AUDIO_STORAGE_BUCKET`, `AUDIO_STORAGE_ACCESS_KEY_ID`, and `AUDIO_STORAGE_SECRET_ACCESS_KEY` configure S3-compatible audio storage.

Do not commit real credentials or `.env` files.

## Verification

Install development tools once with `python -m pip install -r backend/requirements-dev.txt`. Browser checks also need `python -m playwright install chromium`. These tools are not required to run the app itself.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
npm.cmd --prefix frontend test
npm.cmd --prefix frontend run build
node tests/verify_t06_foundation.mjs
.\.venv\Scripts\python.exe scripts/audit_runtime.py
```

The runtime audit is read-only and requires the local backend and dependencies. For browser audit, install `playwright` in the development venv and its Chromium browser, then run `python tests/e2e_audit.py`. It creates/removes a temporary admin and intercepts visitor analytics; it does not use a real account password. See `AUDIT_REPORT_2026-10-21.md` for limitations.

Run `python tests/e2e_admin_workflow.py` separately for the new live workflow, including real Edge TTS, uploaded image, snapshot QR, offline playback and regeneration. It needs Docker/Internet and creates/removes disposable records and storage objects. Run these browser audits sequentially against an idle demo. Expected counts are read from the current database; adding a POI with only one localization is valid and does not require six translations/audio files immediately.
