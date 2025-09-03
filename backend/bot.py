import requests
from bs4 import BeautifulSoup
from backend.ai import query_gemmy

SITES = {
    "F1i": "https://www.f1i.com/news/",
    "Motorsport": "https://www.motorsport.com/f1/news/",
    "NextgenAuto": "https://motorsport.nextgen-auto.com/rubrique/formule-1,3",
    "F1.com": "https://www.formula1.com/en/latest/all.html",
    "PlanetF1": "https://www.planetf1.com/f1-news/",
    "Crash.net": "https://www.crash.net/f1/news",
    "GPFans": "https://www.gpfans.com/en/f1-news/",
    "The Race": "https://www.the-race.com/formula-1/",
    "Autosport": "https://www.autosport.com/f1/news/",
    "ESPN F1": "https://www.espn.com/f1/",
}

validated_articles_cache = []

def generic_scraper(name, url, selector):
    try:
        res = requests.get(url, verify=False, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"Erreur {name}: {e}")
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    return [
        {"title": el.text.strip(), "url": el["href"]}
        for el in soup.select(selector)[:5]
    ]

def get_all_articles():
    articles = []
    articles += generic_scraper("F1i", SITES["F1i"], ".news-list .news-item h3 a")
    articles += generic_scraper("Motorsport", SITES["Motorsport"], ".ms-item_title a")
    articles += generic_scraper("NextgenAuto", SITES["NextgenAuto"], ".titre a")
    articles += generic_scraper("F1.com", SITES["F1.com"], ".f1-latest-listing a.f1-cc")
    articles += generic_scraper("PlanetF1", SITES["PlanetF1"], ".article-card__title a")
    articles += generic_scraper("Crash.net", SITES["Crash.net"], ".title a")
    articles += generic_scraper("GPFans", SITES["GPFans"], ".newslist__title a")
    articles += generic_scraper("The Race", SITES["The Race"], ".article-card__title a")
    articles += generic_scraper("Autosport", SITES["Autosport"], ".ms-item_title a")
    articles += generic_scraper("ESPN F1", SITES["ESPN F1"], ".headlineStack__list li a")
    return articles

def cross_check_articles(articles):
    validated = []
    n = len(articles)
    for i in range(n):
        for j in range(i + 1, n):
            title1, title2 = articles[i]["title"], articles[j]["title"]
            verdict = query_gemmy(f"Ces deux titres F1 parlent-ils de la même info ?\n1: {title1}\n2: {title2}\nRéponds juste par OUI ou NON.")
            if "OUI" in verdict.upper():
                summary = query_gemmy(f"Fais un court résumé de cette info confirmée :\n{title1}\n{title2}")
                validated.append({"summary": summary, "sources": [articles[i]["url"], articles[j]["url"]]})
    return validated

def run_bot():
    global validated_articles_cache
    print("Bot lancé : récupération des articles...")
    articles = get_all_articles()
    validated_articles_cache = cross_check_articles(articles)
    print(f"{len(validated_articles_cache)} articles validés.")

def get_validated_articles():
    return validated_articles_cache
