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

T01 establishes and preserves repository structure only. The runnable React/Vite shell and FastAPI application/health endpoint are separate dependent tasks (T02 and T03) in `IMPLEMENTATION_PLAN.md`; no feature or database behavior belongs in this bootstrap task.
