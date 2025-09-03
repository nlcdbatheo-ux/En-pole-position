from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import threading
import time
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Chemin vers le build du frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/dist")
if not os.path.exists(frontend_path):
    raise RuntimeError(f"Directory '{frontend_path}' does not exist. Build the frontend first!")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# ====== Bot en arrière-plan ======
articles = []

SITES = [
    "https://www.f1i.com",
    "https://f1i.com",
    "https://www.motorsport.com",
    "https://motorsport.nextgen-auto.com",
    "https://www.formula1.com",
    "https://www.crash.net",
    "https://www.gpfans.com",
    "https://www.the-race.com",
]

def fetch_articles():
    while True:
        new_articles = []
        for site in SITES:
            try:
                resp = requests.get(site, timeout=5, verify=False)
                soup = BeautifulSoup(resp.text, "html.parser")
                # Exemple simple : récupérer tous les titres h2
                titles = [h2.get_text(strip=True) for h2 in soup.find_all("h2")]
                for t in titles:
                    new_articles.append({"site": site, "title": t})
            except Exception as e:
                print(f"Erreur site {site}: {e}")
        global articles
        articles = new_articles
        time.sleep(300)  # rafraîchir toutes les 5 minutes

# Lancer le bot en arrière-plan
threading.Thread(target=fetch_articles, daemon=True).start()

# Endpoint pour récupérer les articles
@app.get("/api/articles")
def get_articles():
    return {"articles": articles}
