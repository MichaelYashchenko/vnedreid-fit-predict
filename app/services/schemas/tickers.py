from pydantic import BaseModel


class Ticker(BaseModel):
    ticker: str
    company_name: str
