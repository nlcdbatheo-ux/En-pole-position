from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///articles.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    url = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def add_article(title, url, content):
    session = SessionLocal()
    exists = session.query(Article).filter_by(title=title).first()
    if exists:
        session.close()
        return exists
    article = Article(title=title, url=url, content=content)
    session.add(article)
    session.commit()
    session.refresh(article)
    session.close()
    return article

def get_all_articles():
    session = SessionLocal()
    articles = session.query(Article).order_by(Article.created_at.desc()).all()
    session.close()
    return articles
