
from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import List
from .db import init_db, insert_article, recent_articles, history_since
from .bot import get_all_articles, cross_check
from .ai import unique_key_from_titles

app = FastAPI(title="En Pôle Position API", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dist_dir = (Path(__file__).parent.parent / "frontend" / "dist").resolve()
if dist_dir.exists():
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="frontend")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/validated")
def api_validated(limit: int = 50):
    return recent_articles(limit=limit)

@app.get("/api/history")
def api_history(days: int = Query(3, ge=1, le=60)):
    return history_since(days=days)

def refresh_job():
    articles = get_all_articles()
    clusters = cross_check(articles)
    for c in clusters:
        key = unique_key_from_titles([c["title"]] + c["sources"])
        insert_article(c["title"], c["summary"], c["sources"], key)

@app.post("/api/refresh")
def api_refresh(background: bool = True, tasks: BackgroundTasks = None):
    if background and tasks is not None:
        tasks.add_task(refresh_job)
        return {"status": "refresh_started"}
    refresh_job()
    return {"status": "refreshed"}
