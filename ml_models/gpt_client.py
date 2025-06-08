import json
import os
import time
import requests
import asyncio

from dotenv import load_dotenv

from ml_models.prompt import KEY_WORDS_PROMPT
from ml_models.interp_prompt import INTERP_PROMT

load_dotenv("../.env")


API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')



import httpx

class GptClient:
    def __init__(self, url: str = API_URL, key: str = API_KEY):
        self.url = url
        self.key = key
        self.client = httpx.AsyncClient()

    async def post(self, message: str):
        response = await self.client.post(self.url + '/api/External/PostNewRequest', json={
            "operatingSystemCode": 12,
            "apiKey": self.key,
            "userDomainName": "TeamWVpIIfAjJ0Ka",
            "dialogIdentifier": "test",
            "aiModelCode": 1,
            "Message": message
        })
        return response

    async def get(self):
        response = await self.client.post(self.url + '/api/External/GetNewResponse', json={
            "operatingSystemCode": 12,
            "apiKey": self.key,
            "dialogIdentifier": "test"
        })
        return response

    async def clear(self):
        response = await self.client.post(self.url + '/api/External/CompleteSession', json={
            "operatingSystemCode": 12,
            "apiKey": self.key,
            "dialogIdentifier": "test"
        })
        return response

    async def close(self):
        await self.client.aclose()


class RequestsError(Exception):
    def __init__(self, status_code, message):
        super().__init__(f'Status code: {status_code}, message: {message}')


gpt = GptClient()


async def get_key_words(companies, key_word_prompt=KEY_WORDS_PROMPT):
    prompt = key_word_prompt.format(', '.join(companies))
    await gpt.post(prompt)
    data = None
    start_time = time.time()
    while data is None and time.time() - start_time < 15:
        response = await gpt.get()
        if response.status_code != 200:
            raise RequestsError(response.status_code, response.json())
        data = response.json().get('data', None)
        await asyncio.sleep(0.2)
    if data is None:
        return TimeoutError('Two long request processing')
    await gpt.clear()
    return json.loads(data['lastMessage'])

async def get_interpretation(news_text: str, sentiment: str, sentiment_score: float, ticker: str, interp_prompt=INTERP_PROMT):
    req_text = f"""
    news_text: {news_text},
    sentiment: {sentiment},
    sentiment_score: {sentiment_score},
    ticker: {ticker}
    """
    prompt = interp_prompt.format(req_text)
    await gpt.post(prompt)
    data = None
    start_time = time.time()

    while data is None and time.time() - start_time < 15:
        response = await gpt.get()
        if response.status_code != 200:
            raise RequestsError(response.status_code, response.json())
        data = response.json().get('data', None)
        await asyncio.sleep(0.2)
    if data is None:
        return TimeoutError('Two long request processing')
    await gpt.clear()
    return data['lastMessage']



if __name__ == "__main__":
    print(get_interpretation("Темпы роста рекламной выручки в 4 квартале оказались ниже прогнозов аналитиков, что вызвало вопросы у инвесторов.","negative", 0.8, "YNDX"))
    print(API_URL, API_KEY, KEY_WORDS_PROMPT, sep="\n")
