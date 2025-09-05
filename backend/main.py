from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from backend.bot import scrape_and_store, get_articles

app = FastAPI(title="En Pôle Position - F1 News")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Scraper auto toutes les 10 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_and_store, "interval", minutes=10)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

# --------------------
@app.get("/api/refresh")
def refresh_articles():
    new_articles = scrape_and_store()
    return {"new_articles": new_articles}

@app.get("/api/articles")
def list_articles():
    return {"articles": get_articles()}
