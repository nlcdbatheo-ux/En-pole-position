import requests
from bs4 import BeautifulSoup
from datetime import datetime
from openrouter import OpenRouter  # supposons que c'est l'API Gemini/Flash
import os

# Liste de sites à scraper
SITES = [
    "https://www.f1i.com/news/",
    "https://www.formula1.com/en/latest.html",
    "https://www.motorsport.com/f1/news/",
    "https://www.crash.net/f1/news",
    "https://www.autosport.com/f1/news/",
    "https://www.f1news.com/",
    "https://www.racefans.net/category/formula-1/",
    "https://www.sportskeeda.com/go/formula-1"
]

# Stockage des articles en mémoire pour l'exemple
ARTICLES_DB = []

# Initialisation du client OpenRouter (Gemini/Flash)
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
client = OpenRouter(api_key=OPENROUTER_KEY)

def fetch_articles():
    """Récupère les articles depuis les sites définis."""
    articles = []
    for site in SITES:
        try:
            r = requests.get(site, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            # Exemple générique : tous les liens d'article
            for link in soup.find_all("a", href=True):
                href = link["href"]
                title = link.get_text(strip=True)
                if title and href.startswith("http"):
                    articles.append({
                        "title": title,
                        "url": href,
                        "site": site,
                        "date": datetime.now().isoformat()
                    })
        except Exception as e:
            print(f"Erreur pour {site}: {e}")
    return articles

def ai_reformulate(article_text):
    """Reformule l'article via l'IA Gemini/Flash OpenRouter."""
    prompt = f"Résume et reformule cet article de F1 de manière concise et claire:\n\n{article_text}"
    try:
        response = client.chat.create(
            model="gpt-gemini-1",  # ou gpt-flash-1 selon le modèle
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print(f"Erreur IA: {e}")
        return article_text

def validate_and_store():
    """Récupère, reformule et stocke les articles uniques."""
    global ARTICLES_DB
    fetched = fetch_articles()
    new_articles = []
    for art in fetched:
        # Vérifier doublons basiques par URL
        if not any(a["url"] == art["url"] for a in ARTICLES_DB):
            # Requête IA pour résumé/reformulation
            art["summary"] = ai_reformulate(art["title"])
            ARTICLES_DB.append(art)
            new_articles.append(art)
    return new_articles

def get_articles():
    """Retourne tous les articles stockés, triés par date."""
    return sorted(ARTICLES_DB, key=lambda x: x["date"], reverse=True)
