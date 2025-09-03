# backend/ai.py
# Appel à Gemini via OpenRouter pour résumer un article.
# - Nécessite la variable d'environnement OPENROUTER_API_KEY (sur Render: "Environment > Add secret")
# - Modèle par défaut: google/gemini-2.5-flash (économe en quota)

import os
import requests
from bs4 import BeautifulSoup

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")


def _fetch_article_text(url: str, max_chars: int = 4000) -> str:
    """
    Récupère le contenu texte principal d'un article en suivant l'URL.
    On extrait les paragraphes <p> et on tronque pour ne pas dépasser la limite.
    """
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # Essais de sélecteurs fréquents pour les articles
        candidates = []
        # blocs potentiels
        for sel in [
            "article", ".article", ".post", ".entry-content", ".story", ".content", ".main-content"
        ]:
            block = soup.select_one(sel)
            if block:
                candidates.append(block)

        text = ""
        if candidates:
            # On prend le premier bloc plausible et on concatène ses <p>
            for p in candidates[0].select("p"):
                chunk = p.get_text(" ", strip=True)
                if chunk and len(chunk) > 40:  # on évite les bribes trop courtes
                    text += chunk + "\n"
        else:
            # fallback: tous les <p> de la page
            for p in soup.find_all("p"):
                chunk = p.get_text(" ", strip=True)
                if chunk and len(chunk) > 40:
                    text += chunk + "\n"

        # si vraiment rien
        if not text:
            text = soup.title.get_text(strip=True) if soup.title else url

        return text[:max_chars]
    except Exception:
        # En cas d'échec, on retourne l'URL (au moins) pour ne pas planter
        return url


def summarize_article_by_url(url: str, title_hint: str = "") -> str:
    """
    Résume l'article situé à `url` à l'aide de Gemini via OpenRouter.
    On télécharge le contenu, puis on demande un résumé concis.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY manquant (à configurer dans Render).")

    article_text = _fetch_article_text(url)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    system_prompt = (
        "Tu es un assistant expert en Formule 1. "
        "Tu fais des résumés factuels, clairs et concis (3 à 4 phrases). "
        "Pas d'invention, pas de spéculation."
    )

    user_prompt = (
        f"Titre (si présent): {title_hint}\n\n"
        f"Contenu de l'article:\n{article_text}\n\n"
        "Donne un résumé en 3-4 phrases maximum en français, avec un ton journaliste spécialisé F1."
    )

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=40)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()
