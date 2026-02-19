# Automated AI Article Analyzer

A full-stack mini project that collects a user’s **email** and an **article URL** from a **Streamlit** frontend, sends the request to a **FastAPI** backend, and triggers an **n8n** workflow (via webhook) to automate downstream processing.

---
## Project Demo

📹 **Watch the demo video**: [Project Demo Video](https://drive.google.com/file/d/1nuUUoH8o-r7B2mCnu4G__QLSFpus0GyL/view?usp=sharing)

## Features

- Streamlit UI form with basic **email** and **URL** validation
- FastAPI backend with:
  - request validation
  - `session_id` generation (UUID)
  - webhook payload forwarding to n8n
- Payload sent to n8n includes:
  - `email`
  - `article_url`
  - `session_id`
- Backend **health check** endpoint for quick status verification

---

## Tech Stack

- **Python** 3.10+
- **Streamlit** (frontend)
- **FastAPI** (backend)
- **Uvicorn** (ASGI server)
- **n8n** (Docker Compose)
- **requests**

---

## Project Structure

- `app.py` — Streamlit UI
- `backend/main.py` — FastAPI API
- `docker-compose.yml` — n8n service
- `requirements.txt` — Python dependencies
- `.env` — environment variables (optional)

---

## Prerequisites

- **Conda** (recommended) or Python `venv`
- **Docker Desktop** (required to run n8n via Docker Compose)

---

## Setup (Conda)

```bash
conda create -n aiagent python=3.10 -y
conda activate aiagent
python -m pip install -r requirements.txt
```

---

## Run n8n (Docker)

Start n8n:

```bash
docker compose up -d
```

Open n8n in your browser:

- http://localhost:5678

---

## Run the Backend (FastAPI)

Set the n8n webhook URL and start the backend.

### PowerShell (Windows)

```powershell
$env:N8N_WEBHOOK_URL="http://localhost:5678/webhook/article-agent"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### Backend endpoints

- Health check: http://127.0.0.1:8000/health  
- Process: `POST` http://127.0.0.1:8000/process

---

## Run the Frontend (Streamlit)

Open a **second terminal**, activate the environment, set the backend URL, and run the app.

### PowerShell (Windows)

```powershell
conda activate aiagent
$env:BACKEND_PROCESS_URL="http://127.0.0.1:8000/process"
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Open the app:

- http://127.0.0.1:8501

---

## API Contract

### `POST /process`

**Request body**
```json
{
  "email": "student@example.com",
  "article_url": "https://example.com/article"
}
```

**Response**
```json
{
  "message": "Submitted successfully. n8n workflow has started.",
  "session_id": "generated-uuid"
}
```

---

## Environment Variables

### Backend

- `N8N_WEBHOOK_URL`  
  - Default: `http://localhost:5678/webhook/article-agent`

### Frontend

- `BACKEND_PROCESS_URL`  
  - Default: `http://127.0.0.1:8000/process`

---

## Notes / Troubleshooting

- If your n8n workflow is using a **test webhook** (`/webhook-test/`), the backend may need to fall back to the regular webhook (`/webhook/`) if it receives a **404**.
- If port **8000** is already in use, run the backend on a different port and update `BACKEND_PROCESS_URL` accordingly.

