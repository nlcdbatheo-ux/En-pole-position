from fastapi import FastAPI
from backend import scraper, aggregator, gemini_client, db

app = FastAPI()

@app.get("/")
def home():
    return {"message": "En pole position API"}

@app.get("/news")
def get_news():
    return db.get_all_articles()

@app.post("/generate")
def generate_news():
    infos = scraper.scrape_sites()
    validated = aggregator.validate(infos)
    if validated:
        article = gemini_client.generate_article(validated)
        db.save_article(article)
        return {"status": "ok", "article": article}
    return {"status": "no_new_info"}
