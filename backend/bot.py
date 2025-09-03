import requests
from bs4 import BeautifulSoup
from .database import add_article
from .ai import query_gemmy

# Sources F1
SOURCES = [
    "https://www.f1i.com/news/",
    "https://www.formula1.com/en/latest.html"
]

def fetch_articles():
    articles = []
    for url in SOURCES:
        try:
            # SSL False temporaire pour bypass
            resp = requests.get(url, verify=False, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            for item in soup.find_all("a", limit=5):
                title = item.get_text().strip()
                link = item.get("href")
                if title and link:
                    articles.append({"title": title, "url": link})
        except Exception as e:
            print(f"Erreur sur {url}: {e}")
    return articles

def run_bot():
    print("Bot lancé : récupération des articles...")
    articles = fetch_articles()
    for article in articles:
        summary = query_gemmy(f"Résumé court pour cet article F1 : {article['title']}")
        add_article(article["title"], summary, article["url"])
    print("Bot terminé.")
