# app/routers/news_router.py
from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Optional, List
from app.services.news_service import NewsService
# from app.models.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter()

# Схема ответа для одного новостного элемента
class NewsItem(BaseModel):
    ticker: str
    news_title: str
    news_summary: str
    news_sentiment: str
    news_hype: Optional[float] = None
    news_date: datetime
    news_tags: List[str]

@router.get("/get_ticker_news", response_model=List[NewsItem])
async def get_ticker_news(
    ticker: str,
    date_start: datetime,
    date_end: datetime,
    source_type: Optional[str] = None,
    # db: Session = Depends(get_db)
):
    return await NewsService.fetch_ticker_news(ticker, date_start, date_end, source_type)