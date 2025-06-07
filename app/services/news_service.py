import json
import os
import urllib.request
from urllib.parse import urlencode
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from typing import Set
from dotenv import load_dotenv
from ml_models.gpt_client import get_key_words
from tinkoff.invest import Client
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX, INVEST_GRPC_API
from tinkoff.invest.schemas import PortfolioPosition, InstrumentIdType
from ml_models.news_dedupl import NewsDeduplicator, transformer_embed
import torch
#
# dedup = NewsDeduplicator(embedding_fn=transformer_embed, similarity_threshold=0.7)
# deduped_news = dedup.deduplicate(news)

load_dotenv("../.env")

TOKEN = os.getenv('TOKEN')


async def get_companies_names_by_ticker(tickers, token = TOKEN, regime=INVEST_GRPC_API):
    companies_names = list()
    async with Client(TOKEN, target=INVEST_GRPC_API) as client:
        for ticker in tickers:
            response = client.instruments.get_instrument_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
                class_code='TQBR', # класс или рынок, к которому относится финансовый инструмент
                id=ticker
            )
            instrument = response.instrument
            companies_names.append(instrument.name)
    return companies_names

def get_stocks_info(token, regime=INVEST_GRPC_API) -> Set[PortfolioPosition]:
    user_stocks = set()
    with Client(token, target=regime) as client:
        accounts = client.users.get_accounts().accounts
        for account in accounts:
            portfolio = client.operations.get_portfolio(account_id=account.id)
            stocks = [
                position for position in portfolio.positions
                if position.instrument_type == "share"  # фильтруем только акции
            ]
            for stock in stocks:
                user_stocks.add(stock)
    return user_stocks



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

    def _join_keywords(self, keywords_list: List[str]) -> str:
        new_kw = []
        for x in keywords_list:
            new_kw.append("(" + x + ")")
        res = " OR ".join(new_kw)
        print(res)
        return res

    def _build_get_url(self, query_params: dict) -> str:
        query_string = urlencode(query_params)
        return f"{self.base_url}?{query_string}"

    def get_news(
        self,
        keywords: List[str],
        category: Optional[str] = None,
        lang: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        max_results: Optional[int] = None
    ) -> dict:
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
        print(url)
        try:
            with urllib.request.urlopen(url) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data
        except Exception as e:
            return {"error": str(e), "url": url}


    async def fetch_ticker_news(self, ticker, from_date, to_date, source_type: str = ""):
        companies = await get_companies_names_by_ticker([ticker])
        kws = get_key_words(companies)
        name = companies[0]
        kws_list = kws[name]
        kws_list.append(name)
        print(kws_list)
        news = self.get_news(kws_list, from_date=from_date, to_date=to_date)
        print("news: ", news, sep='\t')
        return news










