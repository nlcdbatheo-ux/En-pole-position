import requests
from bs4 import BeautifulSoup
from .database import save_articles
from .ai import analyze_articles

SOURCES = {
    "Formula1": "https://www.formula1.com/en/latest/all.html",
    "Motorsport": "https://www.motorsport.com/f1/news/",
    "Autosport": "https://www.autosport.com/f1/news/",
    "ESPN F1": "https://www.espn.com/f1/",
    "L'Équipe": "https://www.lequipe.fr/Formule-1/",
}

def scrape_source(name, url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        # extraction simplifiée → faudra ajuster pour chaque site
        items = [a.get_text(strip=True) for a in soup.find_all("a") if a.get_text()]
        return [{"title": t, "url": url, "source": name} for t in items[:10]]
    except Exception as e:
        print(f"[ERREUR scraping {name}] {e}")
        return []

def run_bot():
    raw_articles = []
    for name, url in SOURCES.items():
        raw_articles.extend(scrape_source(name, url))

    validated = analyze_articles(raw_articles)
    save_articles(validated)
