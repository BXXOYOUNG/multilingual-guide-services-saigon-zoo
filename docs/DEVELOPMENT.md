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
