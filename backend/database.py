# backend/database.py
articles = []

def add_article(article: dict):
    articles.append(article)

def get_articles():
    return articles
