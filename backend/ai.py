import os
import requests

API_KEY = os.getenv("MISTRAL_API_KEY")  # mettre la variable d'environnement sur Render
MODEL = "mistral-large"  # ou le nom exact du modèle Mistral que tu as choisi

def query_gemmy(prompt: str) -> str:
    """
    Interroge l'API Mistral pour générer un résumé.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # lèvera une erreur si la requête échoue
    data = response.json()

    # Mistral retourne le texte dans choices[0]["message"]["content"]
    return data["choices"][0]["message"]["content"]
