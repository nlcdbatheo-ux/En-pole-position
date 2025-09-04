import requests
from bs4 import BeautifulSoup

articles_cache = []

sources = [
    "https://www.formula1.com/en/latest",
    "https://www.motorsport.com/f1/news/",
    "https://fr.motorsport.com/f1/news/",
    "https://www.autohebdo.fr/f1/",
    "https://www.nextgen-auto.com/-Formule-1-.html",
    "https://f1i.autojournal.fr/",
    "https://www.lequipe.fr/Formule-1/",
    "https://www.racingnews365.com/formula-1-news",
]

def fetch_and_validate_articles(force_refresh=False):
    global articles_cache

    if articles_cache and not force_refresh:
        return articles_cache

    new_articles = []

    for url in sources:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue

            soup = BeautifulSoup(r.text, "html.parser")

            # récupération simple : tous les titres h1, h2, h3
            for h in soup.find_all(["h1", "h2", "h3"]):
                title = h.get_text(strip=True)
                if title and len(title) > 10:  # éviter les titres trop courts
                    new_articles.append({
                        "title": title,
                        "source": url
                    })

        except Exception as e:
            print(f"Erreur scraping {url} : {e}")

    articles_cache = new_articles
    return articles_cache
