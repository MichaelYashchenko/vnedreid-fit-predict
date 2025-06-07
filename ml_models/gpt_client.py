import json
import os
import time
import requests

from dotenv import load_dotenv

from ml_models.prompt import KEY_WORDS_PROMPT

load_dotenv("../.env")


API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')



class GptClient:
    def __init__(self, url: str = API_URL, key: str = API_KEY):
        self.url = url
        self.key = key

    def post(self, message: str):
        # Отправка запроса
        return requests.post(self.url + '/api/External/PostNewRequest', json={
            "operatingSystemCode": 12,
            "apiKey": self.key,
            "userDomainName": "TeamWVpIIfAjJ0Ka",
            "dialogIdentifier": "test",
            "aiModelCode": 1,
            "Message": message
        })

    def get(self):
        # Забор результатов
        return requests.post(self.url + '/api/External/GetNewResponse', json={
            "operatingSystemCode": 12,
            "apiKey": self.key,
            "dialogIdentifier": "test"
        })

    def clear(self):
        # Очистка контекста
        return requests.post(self.url + '/api/External/CompleteSession', json={
            "operatingSystemCode": 12,
            "apiKey": self.key,
            "dialogIdentifier": "test"
        })


class RequestsError(Exception):
    def __init__(self, status_code, message):
        super().__init__(f'Status code: {status_code}, message: {message}')


gpt = GptClient()


def get_key_words(companies, key_word_prompt=KEY_WORDS_PROMPT):
    prompt = key_word_prompt.format(', '.join(companies))
    gpt.post(prompt)
    data = None
    start_time = time.time()
    while data is None and time.time() - start_time < 15:
        response = gpt.get()
        if response.status_code != 200:
            raise RequestsError(response.status_code, response.json())
        data = response.json().get('data', None)
        time.sleep(0.2)
    if data is None:
        return TimeoutError('Two long request processing')
    gpt.clear()
    return json.loads(data['lastMessage'])


if __name__ == "__main__":
    print(get_key_words(["Газпром"]))
    print(API_URL, API_KEY, KEY_WORDS_PROMPT, sep="\n")
