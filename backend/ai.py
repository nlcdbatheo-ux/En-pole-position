import os
import requests

# On lit la clé API (doit être définie sur Render : MISTRAL_API_KEY)
API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    raise ValueError("❌ La variable d'environnement MISTRAL_API_KEY est manquante !")

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"  # tu peux changer pour "mistralai/mistral-7b-instruct" ou "mistral-large-latest"

def query_gemmy(prompt: str) -> str:
    """
    Envoie un prompt au modèle Mistral via OpenRouter et retourne la réponse texte.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Tu es un assistant qui analyse les actualités de Formule 1."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,   # plus bas = réponses précises
        "max_tokens": 300
    }

    try:
        res = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Erreur API Mistral: {e}")
        return "Erreur lors de l'appel à Mistral."
