from pydantic import BaseModel

class Article(BaseModel):
    id: int
    title: str
    summary: str
    url: str
