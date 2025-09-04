from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from bot import validate_and_store, get_articles

app = FastAPI()

# CORS (pour que le front-end puisse accéder)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Montre le front-end si nécessaire
if os.path.isdir("../frontend/dist"):
    app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")

# Endpoint pour déclencher le scrape / validation
@app.get("/api/validate")
def validate():
    new_articles = validate_and_store()
    return {"new_articles_count": len(new_articles), "new_articles": new_articles}

# Endpoint pour récupérer tous les articles
@app.get("/api/articles")
def articles():
    return get_articles()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
