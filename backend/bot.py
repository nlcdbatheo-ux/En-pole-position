import requests
from bs4 import BeautifulSoup
from database import add_article

# Liste de sites F1 à scraper
NEWS_SOURCES = [
    "https://www.formula1.com/en/latest.html",
    "https://www.f1i.com/news/",
    "https://www.motorsport.com/f1/news/",
    "https://www.autosport.com/f1/news/"
]

def scrape_site(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        # Simple extraction : tous les titres h3 ou a avec class contenant "title"
        articles = []
        for tag in soup.find_all(["h3", "a"]):
            text = tag.get_text(strip=True)
            link = tag.get("href")
            if text and link:
                # Simplification : résume = titre
                articles.append({"title": text, "summary": text, "url": link})
        return articles
    except Exception as e:
        print(f"Erreur scraping {url}: {e}")
        return []

def run_bot():
    for site in NEWS_SOURCES:
        articles = scrape_site(site)
        for a in articles:
            add_article(a["title"], a["summary"], a["url"])
