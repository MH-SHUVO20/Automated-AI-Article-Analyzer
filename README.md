@'
# Automated AI Article Analyzer

A full-stack mini project that accepts an email and article URL from a Streamlit frontend, sends the request to a FastAPI backend, and triggers an n8n workflow for automation.

## Features

- Frontend form with email and URL validation
- Backend input validation and session_id generation
- Payload forwarding to n8n webhook:
  - email
  - article_url
  - session_id
- Health check endpoint for backend status

## Tech Stack

- Python 3.10+
- Streamlit
- FastAPI
- Uvicorn
- n8n (Docker Compose)
- Requests

## Project Structure

- [app.py](http://_vscodecontentref_/1) — Streamlit UI
- [main.py](http://_vscodecontentref_/2) — FastAPI API
- [docker-compose.yml](http://_vscodecontentref_/3) — n8n service
- [requirements.txt](http://_vscodecontentref_/4) — Python dependencies
- .env — environment variables (optional)

## Prerequisites

- Conda (recommended) or Python venv
- Docker Desktop (for n8n)

## Setup (Conda)

conda create -n aiagent python=3.10 -y
conda activate aiagent
python -m pip install -r [requirements.txt](http://_vscodecontentref_/5)

## Run n8n

docker compose up -d

Open n8n at:

- http://localhost:5678

## Run Backend

$env:N8N_WEBHOOK_URL="http://localhost:5678/webhook/article-agent"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

Backend endpoints:

- Health: http://127.0.0.1:8000/health
- Process: POST /process

## Run Frontend

Open a second terminal:

conda activate aiagent
$env:BACKEND_PROCESS_URL="http://127.0.0.1:8000/process"
python -m streamlit run [app.py](http://_vscodecontentref_/6) --server.address 127.0.0.1 --server.port 8501

Open app:

- http://127.0.0.1:8501

## API Contract

POST /process request body:

{
  "email": "student@example.com",
  "article_url": "https://example.com/article"
}

Response:

{
  "message": "Submitted successfully. n8n workflow has started.",
  "session_id": "generated-uuid"
}

## Environment Variables

- N8N_WEBHOOK_URL (backend): default http://localhost:5678/webhook/article-agent
- BACKEND_PROCESS_URL (frontend): default http://127.0.0.1:8000/process

## Notes

- If n8n webhook test URL is used (/webhook-test/), backend can fallback to /webhook/ on 404.
- If port 8000 is busy, run backend on another port and update BACKEND_PROCESS_URL.
'@ | Set-Content -Path [README.md](http://_vscodecontentref_/7) -Encoding UTF8