import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import difflib
from deep_translator import GoogleTranslator

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# --- Liste des sites spécialisés F1 ---
SITES = [
    "https://www.f1i.fr/",
    "https://motorsport.com/f1/news/",
    "https://www.formula1.com/en/latest/all",
    "https://www.autohebdo.fr/f1/",
    "https://www.nextgen-auto.com/-Formule-1-.html",
    "https://fr.motorsport.com/f1/news/",
    "https://www.racingnews365.com/f1-news",
    "https://www.grandprix.com/news.html"
]

# --- Traduction ---
def translate_to_french(text):
    try:
        return GoogleTranslator(source="auto", target="fr").translate(text)
    except Exception:
        return text

# --- Scraping articles ---
def scrape_articles():
    articles = []
    for site in SITES:
        try:
            r = requests.get(site, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            links = soup.find_all("a")
            for link in links[:10]:
                title = link.get_text(strip=True)
                url = link.get("href")
                if title and url:
                    if url.startswith("/"):
                        url = site.rstrip("/") + url
                    articles.append({"title": title, "url": url})
        except Exception as e:
            print(f"Erreur scraping {site}: {e}")
    return articles

# --- Vérifie si deux articles sont similaires ---
def are_similar(text1, text2, threshold=0.6):
    return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio() > threshold

# --- Supprime doublons ---
def deduplicate_articles(articles):
    unique = []
    for art in articles:
        if not any(are_similar(art["title"], u["title"]) for u in unique):
            unique.append(art)
    return unique

# --- Résumé simple ---
def summarize(text, max_sentences=3):
    words = word_tokenize(text.lower())
    sw = set(stopwords.words("english") + stopwords.words("french"))
    words = [w for w in words if w.isalnum() and w not in sw]

    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    sentences = sent_tokenize(text)
    ranking = {}
    for sent in sentences:
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[sent] = ranking.get(sent, 0) + freq[w]

    ranked = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    summary = " ".join([s for s, _ in ranked[:max_sentences]])
    return summary if summary else text

# --- Pipeline principal ---
def process_articles():
    print("🔎 Récupération des articles...")
    raw_articles = scrape_articles()
    articles = deduplicate_articles(raw_articles)

    processed = []
    for art in articles:
        summary = summarize(art["title"])
        summary_fr = translate_to_french(summary)
        processed.append({
            "title": art["title"],
            "url": art["url"],
            "summary": summary_fr
        })
    return processed
