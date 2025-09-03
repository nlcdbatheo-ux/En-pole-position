from fastapi import FastAPI
from backend.bot import run_bot

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("Lancement du bot...")
    run_bot()
    print("Bot lancé : récupération des articles...")

@app.get("/")
def read_root():
    return {"message": "En Pôle Position"}
