# alpha-agent

Monorepo: **Next.js 16** (App Router) frontend + **FastAPI** backend.

**Prerequisites:** Node.js ≥20.9.0 (frontend), Python ≥3.11 + [uv](https://docs.astral.sh/uv/) (backend)

| App      | Command | URL |
|----------|---------|-----|
| Frontend | `cd frontend && npm run dev` | [localhost:3000](http://localhost:3000) |
| Backend  | `cd backend && uv run run-api` | [localhost:8000](http://localhost:8000) · [docs](http://localhost:8000/docs) |

**Backend (uv):** From `backend/`, run `uv sync` once (creates .venv + installs deps), then `uv run run-api`. Or: `uv run uvicorn main:app --reload`.

**Auto-activate venv:** [direnv](https://direnv.net/) is set up in `backend/`. Install it (`brew install direnv`), add [the hook](https://direnv.net/docs/hook.html) to your shell, then run `direnv allow` inside `backend/`. After that, the backend `.venv` activates automatically when you `cd backend`.
