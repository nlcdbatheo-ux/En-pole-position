
import hashlib

def normalize(txt: str) -> str:
    return " ".join(txt.lower().strip().split())

def same_news_heuristic(a: str, b: str) -> bool:
    na, nb = normalize(a), normalize(b)
    if na == nb:
        return True
    seta = set([w for w in na.split() if len(w) > 2])
    setb = set([w for w in nb.split() if len(w) > 2])
    if not seta or not setb:
        return False
    jacc = len(seta & setb) / len(seta | setb)
    return jacc >= 0.45

def summarize_title_pair(a: str, b: str) -> str:
    return a.strip() if len(a) <= len(b) else b.strip()

def unique_key_from_titles(titles):
    base = " || ".join(sorted([normalize(t) for t in titles]))
    return hashlib.sha256(base.encode()).hexdigest()[:32]
