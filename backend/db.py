
import sqlite3
from contextlib import contextmanager
from pathlib import Path
import json
from typing import List

DB_PATH = Path(__file__).parent / "data.db"

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            '''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                summary TEXT,
                sources TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                unique_key TEXT UNIQUE
            )
            '''
        )
        con.commit()

@contextmanager
def get_conn():
    con = sqlite3.connect(DB_PATH)
    try:
        yield con
    finally:
        con.close()

def insert_article(title: str, summary: str, sources: List[str], unique_key: str) -> bool:
    with get_conn() as con:
        try:
            con.execute(
                "INSERT INTO articles (title, summary, sources, unique_key) VALUES (?, ?, ?, ?)",
                (title, summary, json.dumps(sources), unique_key),
            )
            con.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def recent_articles(limit: int = 50):
    with get_conn() as con:
        cur = con.execute(
            "SELECT title, summary, sources, created_at FROM articles ORDER BY datetime(created_at) DESC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
        return [
            {"title": r[0], "summary": r[1], "sources": json.loads(r[2]), "created_at": r[3]}
            for r in rows
        ]

def history_since(days: int = 3):
    with get_conn() as con:
        cur = con.execute(
            '''
            SELECT title, summary, sources, created_at
            FROM articles
            WHERE datetime(created_at) >= datetime('now', ?)
            ORDER BY datetime(created_at) DESC
            ''',
            (f"-{days} days",),
        )
        rows = cur.fetchall()
        return [
            {"title": r[0], "summary": r[1], "sources": json.loads(r[2]), "created_at": r[3]}
            for r in rows
        ]
