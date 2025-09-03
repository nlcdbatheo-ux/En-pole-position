# backend/main.py
# API FastAPI : uniquement scraping et lecture des articles

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import get_articles
from .bot import run_bot

app = FastAPI(title="En Pole Position - API")

# CORS: autorise tout pour simplifier
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Au démarrage, on lance un scraping initial."""
    try:
        print("🚀 Démarrage : scraping initial...")
        run_bot()
        print("✅ Scraping initial terminé")
    except Exception as e:
        print(f"[ERREUR scraping startup] {e}")

@app.get("/articles")
def read_articles():
    """Retourne les articles en mémoire (titres + URLs + source)."""
    return {"articles": get_articles()}

@app.post("/refresh")
def refresh():
    """Permet de relancer manuellement le scraping."""
    try:
        run_bot()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
