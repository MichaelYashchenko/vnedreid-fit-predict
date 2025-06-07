from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime

class Source(BaseModel):
    name: str
    url: HttpUrl

class Article(BaseModel):
    news_title: str
    news_summary: str
    content: str
    url: HttpUrl
    image: HttpUrl
    publishedAt: datetime
    source: str
    duplicates: int
    news_sentiment: str
    news_sentiment_score: float
    news_tags: list[str]

class NewsResponse(BaseModel):
    articles: List[Article]