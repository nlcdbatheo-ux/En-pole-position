
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
from .ai import same_news_heuristic, summarize_title_pair

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36"
}

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
    "ESPN F1": "https://www.espn.com/f1/"
}

def fetch(url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        return r.text, url
    except Exception:
        return None, url

def scrape_f1i() -> List[Dict]:
    html, url = fetch(SITES["F1i"])
    if not html: return []
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for it in soup.select(".news-list .news-item")[:8]:
        a = it.select_one("h3 a")
        if not a: continue
        title = a.get_text(strip=True)
        link = a.get("href")
        items.append({"site": "F1i", "title": title, "link": urljoin(url, link)})
    return items

def scrape_motorsport() -> List[Dict]:
    html, base = fetch(SITES["Motorsport"])
    if not html: return []
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for el in soup.select("a.ms-item_title")[:8]:
        title = el.get_text(strip=True)
        link = el.get("href")
        out.append({"site": "Motorsport", "title": title, "link": urljoin(base, link)})
    return out

def scrape_nextgen() -> List[Dict]:
    html, base = fetch(SITES["NextgenAuto"])
    if not html: return []
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for el in soup.select(".titre a")[:8]:
        out.append({"site": "NextgenAuto", "title": el.get_text(strip=True), "link": urljoin(base, el.get("href"))})
    return out

def generic(name, url, selector) -> List[Dict]:
    html, base = fetch(url)
    if not html: return []
    soup = BeautifulSoup(html, "html.parser")
    res = []
    for a in soup.select(selector)[:8]:
        title = a.get_text(strip=True)
        href = a.get("href")
        if title and href:
            res.append({"site": name, "title": title, "link": urljoin(base, href)})
    return res

def get_all_articles() -> List[Dict]:
    articles: List[Dict] = []
    articles += scrape_f1i()
    articles += scrape_motorsport()
    articles += scrape_nextgen()
    articles += generic("F1.com", SITES["F1.com"], "a.f1-cc, a.f1-cc--clickable")
    articles += generic("PlanetF1", SITES["PlanetF1"], ".article-card__title a")
    articles += generic("Crash.net", SITES["Crash.net"], ".title a")
    articles += generic("GPFans", SITES["GPFans"], ".newslist__title a, article a")
    articles += generic("The Race", SITES["The Race"], ".article-card__title a")
    articles += generic("Autosport", SITES["Autosport"], "a.ms-item_title, .ms-item_title a")
    articles += generic("ESPN F1", SITES["ESPN F1"], ".headlineStack__list a, .headlineStack__list li a")
    # De-dup
    seen = set()
    uniq = []
    for a in articles:
        key = (a["title"], a["link"])
        if key in seen: continue
        seen.add(key)
        uniq.append(a)
    return uniq

def cross_check(articles: List[Dict]) -> List[Dict]:
    groups: List[List[Dict]] = []
    for a in articles:
        placed = False
        for g in groups:
            if any(same_news_heuristic(a["title"], b["title"]) for b in g):
                g.append(a)
                placed = True
                break
        if not placed:
            groups.append([a])

    validated = []
    for g in groups:
        if len(g) < 2:
            continue
        rep_title = g[0]["title"]
        for x in g[1:]:
            rep_title = summarize_title_pair(rep_title, x["title"])
        sources = [x["link"] for x in g]
        validated.append({
            "title": rep_title,
            "summary": rep_title,
            "sources": sources[:6]
        })
    return validated
