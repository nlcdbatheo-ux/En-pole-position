import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def analyze_articles(articles):
    """
    Envoie la liste d'articles à OpenRouter et demande de regrouper + résumer.
    articles = [{ "title": "...", "url": "...", "source": "..." }]
    """
    prompt = f"""
Tu es une IA journaliste spécialisée en F1.
Voici des articles bruts provenant de différents sites :

{articles}

Tâche :
1. Regroupe les articles qui parlent du même sujet (même info, même événement).
2. Si une info apparaît sur au moins 2 sites différents → valide-la.
3. Crée un résumé clair (1 phrase max).
4. Retourne un JSON avec :
[
  {{
    "title": "...",
    "summary": "...",
    "sources": ["url1", "url2"]
  }},
  ...
]
"""
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "google/gemini-1.5-flash",  # rapide et pas cher
            "messages": [
                {"role": "system", "content": "Tu es une IA journaliste F1."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        },
    )
    data = resp.json()
    try:
        text = data["choices"][0]["message"]["content"]
        return eval(text)  # ATTENTION: en vrai, tu devrais parser JSON proprement
    except Exception as e:
        print("Erreur analyse IA:", e, data)
        return []

