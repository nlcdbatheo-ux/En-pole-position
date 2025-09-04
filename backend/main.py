from fastapi import FastAPI
from .bot import fetch_articles, validate_and_store

app = FastAPI(title="F1 News Aggregator")

@app.get("/")
async def root():
    return {"message": "API F1 opérationnelle !"}

@app.get("/articles")
async def get_articles():
    """
    Récupère et valide les articles F1, puis retourne les articles pertinents.
    """
    articles = fetch_articles()
    valid_articles = validate_and_store(articles)
    return {"articles": valid_articles}
