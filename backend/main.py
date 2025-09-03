from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # remplacer par ton URL frontend si nécessaire
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SITES = {
    "F1i": "https://www.f1i.com/news/",
    "Motorsport": "https://www.motorsport.com/f1/news/",
    # ajouter d'autres sites si besoin
}

def scrape_f1i():
    try:
        res = requests.get(SITES["F1i"], verify=False, timeout=10)
        res.raise_for_status()
    except Exception:
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    return [
        {"title": item.select_one("h3 a").text.strip(),
         "url": item.select_one("h3 a")["href"]}
        for item in soup.select(".news-list .news-item")[:5]
    ]

def scrape_motorsport():
    try:
        res = requests.get(SITES["Motorsport"], verify=False, timeout=10)
        res.raise_for_status()
    except Exception:
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    return [
        {"title": item.select_one("a").text.strip(),
         "url": item.select_one("a")["href"]}
        for item in soup.select(".ms-item_title")[:5]
    ]

@app.get("/validated")
async def get_validated_articles():
    articles = scrape_f1i() + scrape_motorsport()
    if not articles:
        return JSONResponse(status_code=404, content={"message": "Aucun article trouvé"})
    return articles
