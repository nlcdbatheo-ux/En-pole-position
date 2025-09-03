import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .ai import summarize_and_compare
from .database import add_article

SITES = [
    "https://www.formula1.com/en/latest.html",
    "https://www.motorsport.com/f1/news/",
    "https://www.f1i.com/news/",
    "https://www.autosport.com/f1/news/",
    "https://www.crash.net/f1/news"
]

def fetch_articles():
    articles = []
    for url in SITES:
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            # Simplifié pour la démo : récupérer tous les titres h3
            for h3 in soup.find_all("h3"):
                title = h3.get_text(strip=True)
                link_tag = h3.find_parent("a")
                link = link_tag["href"] if link_tag else url
                articles.append({"title": title, "url": link, "content": title})
        except Exception as e:
            print(f"Erreur sur {url}: {e}")
    return articles

def run_bot():
    articles = fetch_articles()
    if not articles:
        return
    
    # Regrouper titres similaires
    texts = [a["content"] for a in articles]
    summary = summarize_and_compare(texts)

    # Ajouter chaque article en base (ou le résumé global si tu veux)
    for article in articles:
        add_article(article["title"], article["url"], article["content"])

    print(f"Bot a ajouté {len(articles)} articles.")
