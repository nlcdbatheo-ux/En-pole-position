# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .bot import validate_and_store, get_articles  # import relatif corrigé

app = FastAPI(title="En Pôle Position Backend")

# Autoriser le front-end à faire des requêtes au back-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu peux mettre ton domaine ici pour plus de sécurité
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route pour récupérer les articles validés
@app.get("/api/validated")
async def get_validated_articles():
    try:
        articles = get_articles()  # fonction depuis bot.py
        validated_articles = validate_and_store(articles)  # valider et stocker
        return {"status": "success", "data": validated_articles}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Route test
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Backend running"}

# Montage du front-end statique (Vite build)
app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")
