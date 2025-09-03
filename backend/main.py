# backend/main.py
# API FastAPI: articles + endpoints IA (résumé) + rafraîchissement du scraping

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import get_articles
from .bot import run_bot
from .ai import summarize_article_by_url

app = FastAPI(title="En Pole Position - API + IA")

# CORS: on autorise tout pour simplifier (tu pourras restreindre à ton domaine Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    Démarrage: on lance le scraping 1 fois pour peupler.
    """
    try:
        print("🚀 Démarrage : scraping initial...")
        run_bot()
        print("✅ Scraping initial terminé")
    except Exception as e:
        print(f"[ERREUR scraping startup] {e}")

@app.get("/articles")
def read_articles():
    """
    Retourne les articles en mémoire (titres + URLs + source).
    """
    return {"articles": get_articles()}

@app.post("/summarize")
def summarize(payload: dict):
    """
    Résume un article via IA.
    JSON attendu: { "url": "<url article>", "title": "<titre (optionnel)>" }
    """
    url = payload.get("url")
    title = payload.get("title", "")
    if not url:
        raise HTTPException(status_code=400, detail="Champ 'url' requis.")
    try:
        summary = summarize_article_by_url(url, title_hint=title)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh")
def refresh():
    """
    Relance manuellement le scraping (au cas où tu veux forcer un refresh depuis Render).
    """
    try:
        run_bot()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
