# Developer Guide

## Project layout

This repository is being built as one web client and one FastAPI backend, following the approved modular-monolith architecture. Backend domain modules are kept in the existing `backend/services/` structure; the existing `backend/api/` and `backend/models/` directories are preserved.

- `frontend/src/` — client application structure for app setup, shared components, features, services, state, local data, and service-worker code.
- `backend/api/` — backend API routes (existing directory).
- `backend/models/` — backend model definitions (existing directory).
- `backend/services/` — backend domain services (existing directory and subdirectories).
- `docs/Use-case/` — approved use-case documents.
- `tests/` — automated checks.

## Bootstrap status

T01 establishes and preserves repository structure only. T02 provides the React/Vite shell, and T03 provides the FastAPI application and process health endpoint; no feature or database behavior belongs in these bootstrap tasks.

## Backend

From the repository root, install the backend dependencies and start the development server:

```sh
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload
```

The `GET /health` endpoint returns `{"status":"healthy"}` when the application is running.

### MongoDB and Redis

Set these environment variables to enable the corresponding connections:

- `MONGODB_URI` — MongoDB connection URI.
- `MONGODB_DATABASE` — database name; required together with `MONGODB_URI`.
- `REDIS_URL` — Redis connection URL (`redis://` or `rediss://`).

Both services are optional for local development. When a service is configured, the backend connects and pings it during startup; an invalid configuration or failed connection stops startup with an error. The clients are closed when the application shuts down. The `/health` endpoint remains a process-only check and does not check either service.

Example values (replace the hosts and database with your local setup):

```text
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=saigon_zoo
REDIS_URL=redis://localhost:6379/0
```

The backend reads variables from its process environment. Do not commit real credentials or a `.env` file.
