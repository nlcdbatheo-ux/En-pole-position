# backend/config.py
# Liste des sources d’actualités à scraper.
# Chaque source a un nom, une URL et un type (pour savoir comment scraper).

NEWS_SOURCES = [
    {
        "name": "F1i",
        "url": "https://www.f1i.com/news/",
        "type": "f1i"
    },
    {
        "name": "Formula1",
        "url": "https://www.formula1.com/en/latest/all.html",
        "type": "formula1"
    }
]
