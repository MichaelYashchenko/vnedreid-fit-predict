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
    duplicates_removed: int
    sentiment: str
    score: float
    key_words: list[str]

class NewsResponse(BaseModel):
    articles: List[Article]