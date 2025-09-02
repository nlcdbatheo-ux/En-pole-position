from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, select
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./news.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

articles_table = Table(
    "articles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("summary", String),
    Column("url", String)
)

metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_articles():
    with SessionLocal() as session:
        result = session.execute(select(articles_table)).fetchall()
        return [dict(row) for row in result]

def add_article(title, summary, url):
    with SessionLocal() as session:
        # Vérifie si déjà présent
        existing = session.execute(
            select(articles_table).where(articles_table.c.url == url)
        ).fetchone()
        if existing:
            return False
        session.execute(
            articles_table.insert().values(title=title, summary=summary, url=url)
        )
        session.commit()
        return True
