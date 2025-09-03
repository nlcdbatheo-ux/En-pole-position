from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.bot import run_bot, get_all_articles, cross_check_articles

app = FastAPI(title="En Pole Position API", version="1.0")

# Autoriser le front-end à accéder à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ⚠️ en prod mets ton vrai domaine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """
    Au démarrage du backend, on lance le bot une première fois.
    """
    print("🚀 API démarrée - Lancement du bot en arrière-plan...")
    run_bot()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API En Pole Position 🏎️"}

@app.get("/articles")
def get_articles():
    """
    Retourne les articles bruts (tous sites).
    """
    return get_all_articles()

@app.get("/validated")
def get_validated_articles():
    """
    Retourne uniquement les articles validés par comparaison IA.
    """
    articles = get_all_articles()
    validated = cross_check_articles(articles)
    return validated
