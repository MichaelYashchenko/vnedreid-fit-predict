# app/routers/news_router.py
import os
from datetime import datetime
from typing import Optional, List, Tuple

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.services.schemas.news_response import Article, Interpretation
from typing import List
from app.services.news_service import (
    NewsService,
    get_ticker_prices as get_tp,
    get_user_pf,
    get_interpretation as get_interp
)
from app.services.schemas import NewsResponse, Ticker, InvestmentToken, InterpretationSchema

load_dotenv('../.env')

router = APIRouter()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
news_service = NewsService(NEWS_API_KEY)


@router.get("/get_ticker_news", response_model=List[Article])
@cache(expire=60 * 5)
async def get_ticker_news(
    tickers: str,
    date_start: datetime,
    date_end: datetime,
):
    tickers = [ticker.strip() for ticker in tickers.split(",")]
    return await news_service.fetch_ticker_news(tickers, date_start, date_end)


@router.get("/get_ticker_prices", response_model=List[Tuple[int, float]])
@cache(expire=60 * 5)
async def get_ticker_prices(
        ticker: str,
        date_start: datetime,
        date_end: datetime
):
    return await get_tp(ticker, date_start, date_end)


@router.get("/get_user_portfolio", response_model=List[Ticker])
@cache(expire=60 * 5)
async def get_user_portfolio(token: InvestmentToken = Depends()):
    return await get_user_pf(token.token)


@router.post("/interpret_news", response_model=Interpretation)
@cache(expire=60 * 5)
async def get_interpretation(interpretation: InterpretationSchema = Depends()):
    return await get_interp(
        interpretation.news_text,
        interpretation.sentiment,
        interpretation.sentiment_score,
        interpretation.ticker
    )
