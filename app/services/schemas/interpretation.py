from pydantic import BaseModel


class InterpretationSchema(BaseModel):
    news_text: str
    sentiment: str
    sentiment_score: float
    ticker: str
