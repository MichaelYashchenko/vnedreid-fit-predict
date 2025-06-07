from pydantic import BaseModel


class InvestmentToken(BaseModel):
    token: str
