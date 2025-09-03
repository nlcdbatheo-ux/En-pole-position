import requests

OPENROUTER_API_KEY = "TON_OPENROUTER_API_KEY"
MODEL = "gemini-2.5-flash"

def summarize_and_compare(texts):
    """
    Prend une liste de textes et renvoie un résumé des informations similaires.
    """
    prompt = (
        "Compare ces textes et renvoie un résumé unique en français "
        "des informations similaires ou redondantes. "
        "Ne change pas le sens."
        f"\n\n{texts}"
    )
    
    response = requests.post(
        "https://openrouter.ai/api/v1/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "input": prompt,
            "max_output_tokens": 500
        }
    )
    
    data = response.json()
    return data.get("completion", "").strip()
