import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL = "gemini-2.5-flash"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def are_articles_similar(title1, content1, title2, content2):
    prompt = (
        "Compare these two news articles. "
        "Return True if they convey roughly the same information, else False.\n\n"
        f"Article 1 Title: {title1}\nContent: {content1}\n\n"
        f"Article 2 Title: {title2}\nContent: {content2}\n"
    )
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }
    response = requests.post(OPENROUTER_URL, json=payload, headers=HEADERS)
    response.raise_for_status()
    result = response.json()
    text = result["choices"][0]["message"]["content"].strip().lower()
    return "true" in text

def summarize_article(title, content):
    prompt = (
        "Summarize this news article in 2-3 sentences.\n\n"
        f"Title: {title}\nContent: {content}\n"
    )
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    response = requests.post(OPENROUTER_URL, json=payload, headers=HEADERS)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

