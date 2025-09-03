import os
import requests

OPENROUTER_API_KEY = "APIKEY"  # Ta nouvelle clé
MODEL = "mistral-small-3"      # Le modèle que tu utilises

def query_gemmy(prompt: str) -> str:
    """
    Envoie une requête au modèle Mistral via OpenRouter pour générer une réponse.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Erreur API OpenRouter : {e}")
        return ""

    data = response.json()
    # OpenRouter renvoie souvent la réponse dans choices[0].message.content
    return data["choices"][0]["message"]["content"]
