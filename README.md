# Gate Analysis Dashboard

Vue 3 frontend and FastAPI backend for exploring UBC gatekeeper grade data (DFW / NGMI rankings, faculty heatmaps, course comparisons, and related charts).

## Prerequisites

- **Node.js** 16+ and **npm**
- **Python** 3.9+ (3.10+ recommended)
- Grade data workbook: `gatekeeper_d_cutoff_202223.xlsx` with sheet **`Raw Grade Data`**

## Project layout

| Path | Role |
|------|------|
| `frontend/` | Vue CLI app (dev server + production build) |
| `backend/` | FastAPI API (`/api/...`) |
| `backend/data/` | Default location for the Excel file |

## Data file

Place the workbook here (or set `GATE_EXCEL_PATH` to another absolute path):

```text
backend/data/gatekeeper_d_cutoff_202223.xlsx
```

Override path (optional):

```bash
export GATE_EXCEL_PATH="/absolute/path/to/gatekeeper_d_cutoff_202223.xlsx"
```

---

## Install dependencies

From the repository root.

### Backend (Python)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend (Node)

```bash
cd frontend
npm install
```

---

## Development mode

Run the **API** and **frontend dev server** in two terminals. The frontend defaults to `http://localhost:9000` for API calls (`frontend/src/api.js`).

### Terminal 1 — API (with auto-reload)

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 9000
```

API docs: [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs)

Quick check:

```bash
curl "http://127.0.0.1:9000/api/data/get_faculties"
```

### Terminal 2 — Frontend (hot reload)

```bash
cd frontend
npm run serve
```

Open the URL printed by Vue CLI (usually [http://localhost:8080](http://localhost:8080)).

If the API runs on a different host or port, point the frontend at it before `npm run serve`:

```bash
export VUE_APP_API_BASE_URL="http://127.0.0.1:9000"
npm run serve
```

### Lint (optional)

```bash
cd frontend
npm run lint
```

---

## Production mode

Production is a **built static frontend** plus a **long-running API** (no `--reload`).

### 1. Build the frontend

Set the public API URL **at build time** (Vue CLI bakes `VUE_APP_*` into the bundle):

```bash
cd frontend
export VUE_APP_API_BASE_URL="http://127.0.0.1:9000"   # use your real API URL in deployment
npm run build
```

Output: `frontend/dist/`

### 2. Run the API

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 9000
```

For heavier load, add workers (adjust to CPU count):

```bash
uvicorn main:app --host 0.0.0.0 --port 9000 --workers 4
```

Ensure `GATE_EXCEL_PATH` (if used) and the Excel file are available on the server.

### 3. Serve the static frontend

The repo does not bundle a static file server into FastAPI. Serve `frontend/dist` with any static host, for example:

```bash
cd frontend
npx --yes serve -s dist -l 8080
```

Then open [http://localhost:8080](http://localhost:8080). The browser will call the API at the URL you set in `VUE_APP_API_BASE_URL` when you ran `npm run build`.

**Typical deployment:** reverse proxy (nginx, Caddy, etc.) — `/` → `frontend/dist`, `/api` → uvicorn on port 9000 — with CORS and `VUE_APP_API_BASE_URL` matching the public API origin.

---

## Environment variables

| Variable | Where | Purpose |
|----------|--------|---------|
| `GATE_EXCEL_PATH` | Backend | Absolute path to the grade workbook |
| `VUE_APP_API_BASE_URL` | Frontend (build + dev) | Base URL for API requests (default: `http://localhost:9000`) |

---

## API overview

All routes are under `/api/data/`, for example:

- `GET /api/data/get_faculties`
- `GET /api/data/get_subjects`
- `GET /api/data/get_top_dfw_courses`
- `GET /api/data/get_course_data?course=...`

See interactive docs at `/docs` when the backend is running.
