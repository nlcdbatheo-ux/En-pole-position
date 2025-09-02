from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bot import run_bot
from database import get_articles

app = FastAPI(title="En pole position API")

# Autoriser le frontend à faire fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace par l'URL de ton frontend pour plus de sécurité
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/news")
def get_news():
    run_bot()  # Lance le bot à chaque requête pour obtenir les dernières infos
    return get_articles()
