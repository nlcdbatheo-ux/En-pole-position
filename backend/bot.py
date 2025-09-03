from backend.ai import query_gemmy
from backend.database import get_articles, save_summary

def run_bot():
    """
    Récupère les articles, demande un résumé à Mistral et sauvegarde dans la DB.
    """
    articles = get_articles()
    print("Bot lancé : récupération des articles...")

    for article in articles:
        title = article.get("title")
        if not title:
            continue

        prompt = f"Résumé court pour cet article F1 : {title}"
        summary = query_gemmy(prompt)

        if summary:
            save_summary(article["id"], summary)
            print(f"Résumé ajouté pour : {title}")
        else:
            print(f"Impossible de générer le résumé pour : {title}")
