from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class Source(BaseModel):
    name: str
    url: HttpUrl

class Article(BaseModel):
    url: HttpUrl
    source: str
    news_date: datetime  # или publishedAt, если хотите другое имя
    news_summary: str
    ticker: str
    news_title: str
    duplicates: int
    news_sentiment: str
    news_sentiment_score: float
    key_words: List[str] = []

    id: Optional[int] = None
    # content: Optional[str] = None
    # image: Optional[HttpUrl] = None
    news_tags: List[str] = []

class NewsResponse(BaseModel):
    articles: List[Article]

class Interpretation(BaseModel):
    interpretation: str 