from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from .bot import process_articles

app = FastAPI()
scheduler = BackgroundScheduler()
articles_cache = []

def update_articles():
    global articles_cache
    articles_cache = process_articles()
    print(f"✅ {len(articles_cache)} articles mis à jour")

@app.on_event("startup")
def startup_event():
    update_articles()
    scheduler.add_job(update_articles, "interval", minutes=10)
    scheduler.start()

@app.get("/articles")
def get_articles():
    return articles_cache
