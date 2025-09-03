from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./articles.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_articles():
    session = SessionLocal()
    articles = session.query(Article).order_by(Article.created_at.desc()).all()
    session.close()
    return [{"title": a.title, "content": a.content, "url": a.url, "created_at": a.created_at} for a in articles]

def add_article(title: str, content: str, url: str):
    session = SessionLocal()
    article = Article(title=title, content=content, url=url)
    session.add(article)
    session.commit()
    session.close()
