from backend.ai import query_gemmy
import requests
from bs4 import BeautifulSoup

def get_articles():
    url = "https://www.f1i.com/news/"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    
    articles = []
    for item in soup.select(".news-item"):  # Adapter le sélecteur au site réel
        title = item.select_one(".title").text.strip()
        link = item.select_one("a")["href"]
        articles.append({"title": title, "link": link})
    return articles

def run_bot():
    articles = get_articles()
    for article in articles:
        try:
            summary = query_gemmy(f"Résumé court pour cet article F1 : {article['title']}")
            print(f"Article: {article['title']}")
            print(f"Résumé: {summary}\n")
        except Exception as e:
            print(f"Erreur pour l'article {article['title']}: {e}")
