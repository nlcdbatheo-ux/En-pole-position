import requests
from bs4 import BeautifulSoup
from .ai import query_gemmy

def fetch_articles():
    """
    Récupère les articles F1 depuis les sites.
    """
    urls = ["https://www.f1i.com/news/", "https://www.formula1.com/en/latest.html"]
    articles = []

    for url in urls:
        try:
            res = requests.get(url, verify=False, timeout=10)  # certificat ignoré pour l'instant
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            for item in soup.select("a.article-title"):  # adapte le sélecteur au site réel
                articles.append({"title": item.get_text(), "url": item["href"]})
        except Exception as e:
            print(f"Erreur lors de la récupération de {url}: {e}")
    return articles

def run_bot():
    """
    Lance le bot : récupère les articles, génère un résumé et affiche.
    """
    print("Bot lancé : récupération des articles...")
    articles = fetch_articles()
    for article in articles:
        try:
            summary = query_gemmy(f"Résumé court pour cet article F1 : {article['title']}")
            print(f"{article['title']}\n-> {summary}\n")
        except Exception as e:
            print(f"Erreur AI pour {article['title']}: {e}")
