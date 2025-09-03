import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_articles
from .bot import run_bot

app = FastAPI(title="En Pôle Position API")

# Autoriser le frontend
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/articles")
def articles():
    return get_articles()

@app.on_event("startup")
def startup_event():
    print("Lancement du bot...")
    run_bot()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
