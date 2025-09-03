from fastapi import FastAPI
from .bot import run_bot

app = FastAPI(title="En Pôle Position")

@app.on_event("startup")
def startup_event():
    print("Démarrage de l'application...")
    run_bot()  # lance le bot au démarrage

@app.get("/")
def read_root():
    return {"message": "En Pôle Position API est en ligne"}
