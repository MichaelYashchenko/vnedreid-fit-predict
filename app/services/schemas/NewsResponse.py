from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime

class Source(BaseModel):
    name: str
    url: HttpUrl

class Article(BaseModel):
    title: str
    description: str
    content: str
    url: HttpUrl
    image: HttpUrl
    publishedAt: datetime
    source: Source

class NewsResponse(BaseModel):
    totalArticles: int
    articles: List[Article]