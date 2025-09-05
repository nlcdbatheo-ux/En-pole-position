import requests
from bs4 import BeautifulSoup
import hashlib
import re
import random
import nltk
from datetime import datetime
from googletrans import Translator

# NLTK
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

# Traducteur Google
translator = Translator()

# --------------------
# Base mémoire
articles_db = []

# --------------------
# Sites spécialisés F1
NEWS_SITES = [
    "https://fr.motorsport.com/f1/news/",
    "https://www.formula1.com/en/latest/all.html",
    "https://www.f1i.fr/",
    "https://www.nextgen-auto.com/-Formule-1-.html",
    "https://www.autohebdo.fr/f1/",
    "https://www.confidential-renault.fr/",
    "https://f1only.fr/",
    "https://www.caradisiac.com/f1/"
]

# --------------------
# Mots-clés
KEYWORDS = [
    "formule 1", "f1", "grand prix", "verstappen", "hamilton", "leclerc",
    "ferrari", "red bull", "mercedes", "mclaren", "aston martin", "alpine"
]

def fetch_html(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return response.text
    except Exception:
        return None
    return None

def extract_articles_from_site(url):
    html = fetch_html(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    articles = []

    for link in soup.find_all("a", href=True):
        title = link.get_text(strip=True)
        href = link["href"]

        if not title or len(title) < 20:
            continue

        if href.startswith("/"):
            href = url.rstrip("/") + href

        if any(kw.lower() in title.lower() for kw in KEYWORDS):
            articles.append({"title": title, "url": href})

    return articles

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return " ".join(text.split())

def get_hash(text):
    return hashlib.md5(normalize_text(text).encode()).hexdigest()

def are_similar(text1, text2):
    set1, set2 = set(normalize_text(text1).split()), set(normalize_text(text2).split())
    common = set1 & set2
    return len(common) / max(len(set1), 1) > 0.4

def synonymize_word(word):
    synsets = wordnet.synsets(word, lang="fra")
    if synsets:
        lemmas = synsets[0].lemma_names("fra")
        if lemmas:
            return random.choice(lemmas)
    return word

def reformulate(text):
    sentences = sent_tokenize(text, language="french")
    reformulated = []
    for sent in sentences:
        words = word_tokenize(sent, language="french")
        new_words = []
        for w in words:
            if random.random() < 0.1:
                new_words.append(synonymize_word(w))
            else:
                new_words.append(w)
        reformulated.append(" ".join(new_words))
    return " ".join(reformulated)

def summarize(text, max_sentences=2):
    """Résumé très simple: garder les premières phrases"""
    sentences = sent_tokenize(text, language="french")
    return " ".join(sentences[:max_sentences])

def translate_to_french(text):
    try:
        detected = translator.detect(text).lang
        if detected != "fr":
            return translator.translate(text, src=detected, dest="fr").text
    except Exception:
        return text
    return text

def scrape_and_store():
    global articles_db
    scraped_articles = []

    for site in NEWS_SITES:
        scraped_articles.extend(extract_articles_from_site(site))

    validated = []
    for art in scraped_articles:
        h = get_hash(art["title"])

        if any(a["hash"] == h for a in articles_db):
            continue

        if any(are_similar(a["title"], art["title"]) for a in articles_db):
            continue

        # Traduire si anglais
        title = translate_to_french(art["title"])

        # Reformuler
        new_title = reformulate(title)

        # Résumer
        summary = summarize(new_title)

        validated.append({
            "title": new_title,
            "summary": summary,
            "url": art["url"],
            "date": datetime.utcnow().isoformat(),
            "hash": h
        })

    articles_db.extend(validated)
    return validated

def get_articles():
    return articles_db
