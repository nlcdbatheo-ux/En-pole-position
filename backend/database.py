# backend/database.py
# Stockage très simple : une liste Python en mémoire.
# Plus tard, tu pourras remplacer ça par une vraie base de données.

articles_storage = []  # Liste d’articles stockés en mémoire

def add_article(article: dict):
    """
    Ajoute un article à la liste.
    """
    articles_storage.append(article)

def get_articles():
    """
    Retourne tous les articles stockés.
    """
    return articles_storage
