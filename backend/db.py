import sqlite3
from datetime import datetime

DB_NAME = "database/news.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            created_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_article(article):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO articles (title, content, created_at) VALUES (?, ?, ?)",
              (article["title"], article["content"], datetime.now()))
    conn.commit()
    conn.close()

def get_all_articles():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, content, created_at FROM articles ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "content": r[2], "created_at": r[3]} for r in rows]

init_db()
