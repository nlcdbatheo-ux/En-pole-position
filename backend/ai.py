import requests
import os

GEMMY_API_KEY = os.environ.get("GEMMY_API_KEY")
GEMMY_MODEL = "2.5-flash"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def query_gemmy(prompt: str):
    headers = {
        "Authorization": f"Bearer {GEMMY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GEMMY_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    response = requests.post(OPENROUTER_URL, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    # Retourne le texte du message généré
    return result["choices"][0]["message"]["content"]
