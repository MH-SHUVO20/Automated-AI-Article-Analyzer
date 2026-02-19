import os
import re
import uuid

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from requests import RequestException

app = FastAPI(
    title="Automated AI Article Analyzer Backend",
    description="Receives article requests and forwards them to the n8n webhook.",
)

EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


class ArticleRequest(BaseModel):
    email: str
    article_url: str


def _is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email.strip()))


def _is_valid_article_url(url: str) -> bool:
    normalized = url.strip().lower()
    return normalized.startswith("http://") or normalized.startswith("https://")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/process")
def process_article(data: ArticleRequest):
    if not _is_valid_email(data.email):
        raise HTTPException(status_code=422, detail="Please provide a valid email address.")

    if not _is_valid_article_url(data.article_url):
        raise HTTPException(status_code=422, detail="Article URL must start with http:// or https://")

    n8n_webhook_url = os.getenv(
        "N8N_WEBHOOK_URL",
        "http://localhost:5678/webhook/article-agent",
    )

    session_id = str(uuid.uuid4())
    payload = {
        "email": data.email.strip(),
        "article_url": data.article_url.strip(),
        "session_id": session_id,
    }

    attempted_urls = [n8n_webhook_url]

    try:
        response = requests.post(
            n8n_webhook_url,
            json=payload,
            timeout=20,
        )

        if response.status_code == 404 and "/webhook-test/" in n8n_webhook_url:
            fallback_url = n8n_webhook_url.replace("/webhook-test/", "/webhook/", 1)
            attempted_urls.append(fallback_url)
            response = requests.post(
                fallback_url,
                json=payload,
                timeout=20,
            )

        response.raise_for_status()
    except RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail="Could not send the request to n8n right now. Please check webhook settings and try again.",
        )

    return {
        "message": "Submitted successfully. n8n workflow has started.",
        "session_id": session_id,
    }
