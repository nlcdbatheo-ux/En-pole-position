from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import nltk
from .bot import process_articles

app = FastAPI()
scheduler = BackgroundScheduler()
articles_cache = []

def update_articles():
    global articles_cache
    try:
        articles_cache = process_articles()
        print(f"✅ {len(articles_cache)} articles mis à jour")
    except Exception as e:
        print(f"⚠️ Erreur lors de la mise à jour des articles: {e}")

@app.on_event("startup")
def startup_event():
    # Téléchargement NLTK uniquement au démarrage
    try:
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
    except Exception as e:
        print(f"⚠️ Impossible de télécharger les modèles NLTK: {e}")

    # Premier run sécurisé
    update_articles()

    # Relance toutes les 10 minutes
    scheduler.add_job(update_articles, "interval", minutes=10)
    scheduler.start()

@app.get("/articles")
def get_articles():
    return articles_cache
