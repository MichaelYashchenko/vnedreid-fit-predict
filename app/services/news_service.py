import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from typing import Set
from urllib.parse import urlencode

from dotenv import load_dotenv
from tinkoff.invest import AsyncClient, CandleInterval
from tinkoff.invest.constants import INVEST_GRPC_API
from tinkoff.invest.schemas import PortfolioPosition, InstrumentIdType
from ml_models.news_dedupl import deduplicate_news
from ml_models.news_relevance import get_news_relevance
from ml_models.news_ner import ner_news
from tinkoff.invest.utils import quotation_to_decimal
from app.services.schemas import Ticker

from ml_models.gpt_client import get_key_words

load_dotenv("../.env")

TOKEN = os.getenv('TOKEN')


async def get_companies_names_by_ticker(tickers, token = TOKEN, regime=INVEST_GRPC_API):
    companies_names = list()
    async with AsyncClient(TOKEN, target=INVEST_GRPC_API) as client:
        for ticker in tickers:
            response = await client.instruments.get_instrument_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
                class_code='TQBR', # класс или рынок, к которому относится финансовый инструмент
                id=ticker
            )
            instrument = response.instrument
            companies_names.append(instrument.name)
    return companies_names

async def get_stocks_info(token=TOKEN, regime=INVEST_GRPC_API) -> Set[PortfolioPosition]:
    user_stocks = set()
    async with AsyncClient(token, target=regime) as client:
        accounts = await client.users.get_accounts()
        for account in accounts.accounts:
            portfolio = await client.operations.get_portfolio(account_id=account.id)
            stocks = [
                position for position in portfolio.positions
                if position.instrument_type == "share"  # фильтруем только акции
            ]
            for stock in stocks:
                user_stocks.add(stock)
    return user_stocks


async def get_user_pf(token):
    user_stocks = await get_stocks_info(token)
    tickers = [stock.ticker for stock in user_stocks]
    companies_names = await get_companies_names_by_ticker(tickers)
    return [
        Ticker(ticker=ticker, company_name=company)
        for ticker, company in zip(tickers, companies_names)
    ]


def quotation_to_float(quotation):
    return round(float(quotation_to_decimal(quotation)), 2)


async def get_ticker_prices(ticker, start_time, end_time, token=TOKEN, regime=INVEST_GRPC_API):
    candles = []
    async with AsyncClient(token, target=regime) as client:
        instrument_response = await client.instruments.get_instrument_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
            class_code='TQBR',  # Main trading mode for stocks
            id=ticker
        )
        instrument_figi = instrument_response.instrument.figi
        async for candle in client.get_all_candles(
            figi=instrument_figi,
            from_=start_time,
            to=end_time,
            interval=CandleInterval.CANDLE_INTERVAL_DAY
        ):
            candles.append(candle)
        if not candles:
            return [[]]
    times = [int(candle.time.timestamp()) for candle in candles]
    prices = [quotation_to_float(candle.close) for candle in candles]
    return list(zip(times, prices))


class NewsService:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://gnews.io/api/v4/search",
        default_lang: str = "ru",
        default_category: str = "general",
        max_results: int = 10,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.default_lang = default_lang
        self.default_category = default_category
        self.max_results = max_results
        self.timezone = timezone(timedelta(hours=3))  # GMT+3 (Москва)

    def _start_of_current_day(self) -> datetime:
        now = datetime.now(self.timezone)
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

    def _current_time(self) -> datetime:
        return datetime.now(self.timezone)

    def _get_iso_format(self, dt: datetime) -> str:
        dt = dt.replace(tzinfo=self.timezone)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def _join_keywords(keywords_list: List[str]) -> str:
        new_kw = []
        for x in keywords_list:
            new_kw.append("(" + x + ")")
        res = " OR ".join(new_kw)
        return res

    def _build_get_url(self, query_params: dict) -> str:
        query_string = urlencode(query_params)
        return f"{self.base_url}?{query_string}"

    def get_news(
        self,
        ticker: str,
        keywords: List[str],
        category: Optional[str] = None,
        lang: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        max_results: Optional[int] = None
    ):
        query_params = {
            "q": self._join_keywords(keywords),
            "category": category or self.default_category,
            "max": max_results or self.max_results,
            "lang": lang or self.default_lang,
            "country": (lang or self.default_lang),
            "from": self._get_iso_format(from_date or self._start_of_current_day()),
            "to": self._get_iso_format(to_date or self._current_time()),
            "apikey": self.api_key,
        }

        url = self._build_get_url(query_params)

        try:
            with urllib.request.urlopen(url) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                articles = data['articles']
                articles = preprocess_articles(ticker, articles)
                return articles
        except Exception as e:
            return []
    def get_news_batch(self, dict_ticker_kws, from_date, to_date):
        result_news = []
        for ticker, kws in dict_ticker_kws.items():
            current_ticker_news = self.get_news(ticker, kws, from_date=from_date, to_date=to_date)
            result_news.extend(current_ticker_news)
        return result_news

    async def fetch_ticker_news(self, tickers, from_date, to_date):
        dict_ticker_kws = dict() # { "GAZP" : ["Газпром", "газ", "природные ресурсы", ... ], "SBER": [ "Герман Греф", "Сбер-тех", "Гигачад"}
        for ticker in tickers:
            companies = await get_companies_names_by_ticker([ticker])#await get_companies_names_by_ticker(tickers)
            kws = get_key_words(companies)
            name = companies[0]
            kws_list = kws[name]
            kws_list.append(name)
            dict_ticker_kws[ticker] = kws_list

        news = self.get_news_batch(dict_ticker_kws, from_date=from_date, to_date=to_date)
        unique_news = deduplicate_news(news)
        with_relevance = get_news_relevance(unique_news)
        nered_news = ner_news(with_relevance)
        return nered_news


def preprocess_articles(ticker, articles_list):
    for _id, article in enumerate(articles_list):
        article['news_date'] = article['publishedAt']
        article['news_summary'] = article['description']
        article['source'] = article['source']['name']
        article['ticker'] = ticker
        article['news_title'] = article['title']
        article['id'] = _id
        del article['publishedAt']
        del article['description']
        del article['title']
        del article['content']
        del article['image']
    return articles_list
