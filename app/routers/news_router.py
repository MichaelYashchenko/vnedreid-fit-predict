# app/routers/news_router.py
import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter

from app.services.news_service import NewsService
from app.services.schemas import NewsResponse

load_dotenv('../.env')

router = APIRouter()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
news_service = NewsService(NEWS_API_KEY)


@router.get("/get_ticker_news", response_model=NewsResponse)
async def get_ticker_news(
    ticker: str,
    date_start: datetime,
    date_end: datetime,
    source_type: Optional[str] = None,
    # db: Session = Depends(get_db)
):
    return await news_service.fetch_ticker_news(ticker, date_start, date_end, source_type)
