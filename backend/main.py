from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_all_articles
from .bot import run_bot
import threading
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adapter si besoin
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/articles")
def read_articles():
    return get_all_articles()

def start_bot_loop():
    while True:
        try:
            run_bot()
        except Exception as e:
            print(f"Erreur bot: {e}")
        time.sleep(60*30)  # toutes les 30 minutes

threading.Thread(target=start_bot_loop, daemon=True).start()
