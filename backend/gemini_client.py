import os
import httpx

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "google/gemini-2.5-flash"

def generate_article(info):
    prompt = f"""Écris un court article journalistique sur la Formule 1 :
    Sujet : {info}
    Donne un titre accrocheur + 5 à 10 phrases de contenu.
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/ton-projet", 
        "X-Title": "En pole position"
    }

    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    article = data["choices"][0]["message"]["content"]
    return {"title": article.split("\n")[0], "content": article}
