import os
import requests

# Lire la clé depuis la variable d'environnement Render
API_KEY = os.getenv("APIKEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistral"  # Nom du modèle Mistral sur OpenRouter

def query_gemmy(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(OPENROUTER_URL, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()

    # Retourner le texte de la réponse du modèle
    return result["choices"][0]["message"]["content"]
