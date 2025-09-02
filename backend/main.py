from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .bot import run_bot      # import relatif, nécessite __init__.py dans backend/
from .database import get_articles

app = FastAPI(title="En pole position API")

# Autoriser le frontend à accéder à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu peux mettre l'URL de ton frontend pour plus de sécurité
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/news")
def get_news():
    """
    Route principale pour récupérer les dernières news.
    À chaque appel, le bot va scrapper les sites et ajouter les nouvelles infos à la base.
    """
    run_bot()  # Lance le bot pour obtenir les dernières infos
    return get_articles()  # Récupère et renvoie toutes les news de la base
