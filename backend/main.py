# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .bot import get_articles, validate_and_store  # import relatif correct

app = FastAPI()

# Autoriser le front (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu peux restreindre si tu veux
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/articles")
def read_articles():
    """Récupère et retourne les articles scrapés"""
    articles = get_articles()
    return {"articles": articles}

@app.post("/validate")
def validate_article(article: dict):
    """Valide un article via l'IA"""
    text = article.get("text", "")
    validated = validate_and_store(text)
    if validated:
        return {"validated_text": validated}
    return {"error": "Impossible de valider l'article"}

