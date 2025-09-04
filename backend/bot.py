import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Clé API Mistral / OpenRouter
API_KEY = os.getenv("MISTRAL_API_KEY")
API_URL = "https://api.openrouter.ai/v1/completions"  # Exemple, selon ton plan OpenRouter

# Liste de sites spécialisés Formule 1
F1_SITES = [
    "https://www.formula1.com/",
    "https://www.f1i.com/",
    "https://fr.motorsport.com/f1/",
    "https://www.racefans.net/category/formula-1/",
    "https://www.autosport.com/f1/",
    "https://www.crash.net/f1",
    "https://www.f1only.fr/",
    "https://www.gpblog.com/en/news/f1.html"
]

def fetch_articles():
    """
    Récupère les titres et liens des articles récents de chaque site.
    """
    articles = []
    for url in F1_SITES:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Exemple générique : on prend tous les liens <a> avec un texte > 20 caractères
            for a in soup.find_all("a"):
                if a.text and len(a.text.strip()) > 20:
                    link = a.get("href")
                    if link and link.startswith("http"):
                        articles.append({"title": a.text.strip(), "url": link})
        except Exception as e:
            print(f"Erreur lors de la récupération de {url}: {e}")
    return articles

def validate_and_store(articles):
    """
    Envoie les articles à OpenRouter pour validation et les stocke si pertinents.
    """
    valid_articles = []
    for article in articles:
        prompt = f"Est-ce que cet article est pertinent pour la Formule 1 ? Répondre par oui ou non.\n\nTitre: {article['title']}\nLien: {article['url']}"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral",  # à ajuster selon ton modèle
            "prompt": prompt,
            "max_tokens": 10
        }
        try:
            r = requests.post(API_URL, json=data, headers=headers, timeout=10)
            r.raise_for_status()
            response = r.json()
            answer = response.get("choices", [{}])[0].get("text", "").lower()
            if "oui" in answer or "yes" in answer:
                valid_articles.append(article)
        except Exception as e:
            print(f"Erreur OpenRouter pour {article['url']}: {e}")
    
    # Stockage simple dans un fichier JSON
    import json
    with open("validated_articles.json", "w", encoding="utf-8") as f:
        json.dump(valid_articles, f, ensure_ascii=False, indent=2)
    
    return valid_articles
