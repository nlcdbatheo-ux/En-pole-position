# backend/main.py
# API FastAPI qui expose les articles scrapés.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_articles
from .bot import run_bot

app = FastAPI(title="En Pole Position - API")

# Autoriser les appels depuis le frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod → limiter au domaine du frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    Quand le backend démarre, on lance immédiatement le scraping.
    """
    print("🚀 Démarrage : lancement du bot de scraping")
    run_bot()
    print("✅ Scraping terminé, API prête")

@app.get("/articles")
def read_articles():
    """
    Endpoint GET /articles → retourne tous les articles
    """
    return {"articles": get_articles()}
