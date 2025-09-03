# backend/bot.py
# Scraper qui va chercher des articles sur les sites listés dans config.py

import requests
from bs4 import BeautifulSoup
from .database import add_article
from .config import NEWS_SOURCES

def run_bot():
    """
    Lance le scraping sur toutes les sources définies dans config.py
    et ajoute les articles en mémoire via add_article().
    """
    for source in NEWS_SOURCES:
        url = source["url"]
        site_type = source["type"]
        site_name = source["name"]

        print(f"🔎 Scraping {site_name} ({url})...")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            if site_type == "f1i":
                for item in soup.select("h2.entry-title a"):
                    article = {
                        "title": item.get_text(strip=True),
                        "url": item["href"],
                        "source": site_name
                    }
                    add_article(article)

            elif site_type == "formula1":
                for item in soup.select("a.f1-cc--caption"):
                    article = {
                        "title": item.get_text(strip=True),
                        "url": "https://www.formula1.com" + item["href"],
                        "source": site_name
                    }
                    add_article(article)

            print(f"✅ {site_name} : {len(get_articles())} articles au total")

        except Exception as e:
            print(f"[ERREUR] {site_name} : {e}")
