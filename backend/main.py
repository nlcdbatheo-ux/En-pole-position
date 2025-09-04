from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.bot import fetch_and_validate_articles

app = FastAPI(title="🏎️ En Pôle Position API")

# CORS pour autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test basique
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

# Endpoint qui renvoie les articles validés
@app.get("/api/validated")
def get_validated():
    return fetch_and_validate_articles()

# Endpoint pour forcer un refresh
@app.get("/api/refresh")
def refresh():
    return fetch_and_validate_articles(force_refresh=True)
