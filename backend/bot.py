# backend/bot.py
import os
import requests
from bs4 import BeautifulSoup
from openrouter import OpenRouterClient
from dotenv import load_dotenv

load_dotenv()

# Initialisation du client OpenRouter avec la clé Mistral
API_KEY = os.getenv("MISTRAL_API_KEY")
client = OpenRouterClient(api_key=API_KEY)

# Liste exacte des sites à scraper
SITES = [
    "https://www.auto-moto.com",
    "https://www.caradisiac.com",
    "https://www.largus.fr",
    "https://www.motorlegend.com",
    "https://www.automobile-sportive.com"
]

def get_articles():
    """Scrape les articles des sites définis et retourne une liste."""
    articles = []
    for site in SITES:
        try:
            r = requests.get(site)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            # exemple : récupérer tous les <h2> comme titres
            for h2 in soup.find_all("h2"):
                articles.append(h2.get_text(strip=True))
        except Exception as e:
            print(f"Erreur sur {site}: {e}")
    return articles

def validate_and_store(article_text):
    """Envoie le texte à l'IA pour validation ou enrichissement, retourne le résultat."""
    try:
        response = client.completions.create(
            model="gemini-1",  # ou "flash" si tu veux Flash
            messages=[
                {"role": "system", "content": "Tu es un assistant qui valide le texte."},
                {"role": "user", "content": article_text}
            ],
            max_tokens=500
        )
        # Récupération du texte renvoyé par le modèle
        validated_text = response.choices[0].message["content"]
        return validated_text
    except Exception as e:
        print(f"Erreur IA: {e}")
        return None
