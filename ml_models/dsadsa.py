# mock_server.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import time
import random

app = Flask(__name__)
CORS(app)

# ОБНОВЛЕННЫЕ И РАСШИРЕННЫЕ ДАННЫЕ: все даты проверены и приходятся на будние дни
mock_news = [
    # SBER (все даты - будни)
    {
        "id": 1,
        "ticker": "SBER",
        "news_title": "Сбербанк анонсировал новую программу лояльности",
        "news_summary": "Новая программа 'СберСпасибо 2.0' предложит повышенный кешбэк в ключевых категориях для активных клиентов.",
        "news_sentiment": "positive",
        "news_sentiment_score": 0.92,
        "news_date": "2024-11-18T11:00:00",
        "source": "РБК",
        "url": "https://www.rbc.ru/finances/...",
        "news_tags": ["лояльность", "кешбэк"],
    },
    {
        "id": 2,
        "ticker": "SBER",
        "news_title": "Аналитики Moody's подтвердили рейтинг Сбербанка",
        "news_summary": "Рейтинговое агентство Moody's подтвердило кредитный рейтинг банка на уровне Baa3 со стабильным прогнозом.",
        "news_sentiment": "neutral",
        "news_sentiment_score": 0.85,
        "news_date": "2024-12-09T15:00:00",
        "source": "Интерфакс",
        "url": "https://www.interfax.ru/business/...",
        "news_tags": ["рейтинг", "Moody's"],
    },
    {
        "id": 11,
        "ticker": "SBER",
        "news_title": "Сбер представил GigaChat Pro для бизнеса",
        "news_summary": "Корпоративная версия нейросети GigaChat стала доступна для бизнес-клиентов с расширенными возможностями интеграции.",
        "news_sentiment": "positive",
        "news_sentiment_score": 0.88,
        "news_date": "2025-01-22T10:30:00",
        "source": "CNews",
        "url": "https://www.cnews.ru/news/...",
        "news_tags": ["ai", "GigaChat", "технологии"],
    },
    {
        "id": 12,
        "ticker": "SBER",
        "news_title": "Технический сбой затронул мобильное приложение Сбербанка",
        "news_summary": "Некоторые пользователи испытывали трудности со входом в приложение в течение часа. Работоспособность полностью восстановлена.",
        "news_sentiment": "negative",
        "news_sentiment_score": 0.70,
        "news_date": "2025-02-13T09:45:00",
        "source": "ТАСС",
        "url": "https://tass.ru/ekonomika/...",
        "news_tags": ["сбой", "приложение"],
    },
    # GAZP (все даты - будни)
    {
        "id": 3,
        "ticker": "GAZP",
        "news_title": "Газпром договорился о поставках газа в Венгрию",
        "news_summary": "Подписан долгосрочный контракт на поставку 4.5 млрд кубометров газа в год, диверсифицируя маршруты поставок.",
        "news_sentiment": "positive",
        "news_sentiment_score": 0.90,
        "news_date": "2024-10-29T14:00:00",
        "source": "Интерфакс",
        "url": "https://www.interfax.ru/business/...",
        "news_tags": ["контракт", "венгрия", "газ"],
    },
    {
        "id": 4,
        "ticker": "GAZP",
        "news_title": "Строительство Амурского ГПЗ идет с опережением графика",
        "news_summary": "Строительная готовность проекта превысила 85%, запуск первых линий ожидается раньше запланированного срока.",
        "news_sentiment": "positive",
        "news_sentiment_score": 0.88,
        "news_date": "2024-11-26T10:00:00",
        "source": "Коммерсантъ",
        "url": "https://www.kommersant.ru/doc/...",
        "news_tags": ["гпз", "строительство"],
    },
    {
        "id": 13,
        "ticker": "GAZP",
        "news_title": "Газпром сократил инвестиционную программу на 2025 год",
        "news_summary": "В связи с изменением рыночной конъюнктуры, компания скорректировала объем инвестиций, оптимизируя расходы.",
        "news_sentiment": "negative",
        "news_sentiment_score": 0.78,
        "news_date": "2024-12-19T18:00:00",
        "source": "Ведомости",
        "url": "https://www.vedomosti.ru/business/...",
        "news_tags": ["инвестиции", "оптимизация"],
    },
    # YNDX (все даты - будни)
    {
        "id": 5,
        "ticker": "YNDX",
        "news_title": "Яндекс.Такси запускает сервис в двух новых странах Латинской Америки",
        "news_summary": "Экспансия на международные рынки продолжается, компания видит большой потенциал для роста в регионе.",
        "news_sentiment": "positive",
        "news_sentiment_score": 0.98,
        "news_date": "2024-11-07T12:00:00",
        "source": "The Bell",
        "url": "https://thebell.io/...",
        "news_tags": ["экспансия", "такси"],
    },
    {
        "id": 6,
        "ticker": "YNDX",
        "news_title": "Яндекс продает медиа-активы 'Дзен' и 'Новости'",
        "news_summary": "Сделка по продаже медийных сервисов VK закрыта. Яндекс фокусируется на развитии поиска, облака и беспилотников.",
        "news_sentiment": "neutral",
        "news_sentiment_score": 0.85,
        "news_date": "2024-09-12T09:00:00",
        "source": "РБК",
        "url": "https://www.rbc.ru/technology_and_media/...",
        "news_tags": ["сделка", "vk", "дзен"],
    },
    {
        "id": 14,
        "ticker": "YNDX",
        "news_title": "Яндекс открыл исходный код библиотеки для машинного обучения CatBoost 2.0",
        "news_summary": "Новая версия библиотеки работает значительно быстрее и включает в себя инструменты для анализа больших данных.",
        "news_sentiment": "positive",
        "news_sentiment_score": 0.95,
        "news_date": "2025-01-30T17:00:00",
        "source": "Хабр",
        "url": "https://habr.com/ru/company/yandex/...",
        "news_tags": ["open-source", "ml", "catboost"],
    },
    {
        "id": 15,
        "ticker": "YNDX",
        "news_title": "Рекламная выручка Яндекса показала замедление роста",
        "news_summary": "Темпы роста рекламной выручки в 4 квартале оказались ниже прогнозов аналитиков, что вызвало вопросы у инвесторов.",
        "news_sentiment": "negative",
        "news_sentiment_score": 0.80,
        "news_date": "2025-02-20T13:00:00",
        "source": "Коммерсантъ",
        "url": "https://www.kommersant.ru/doc/...",
        "news_tags": ["отчетность", "реклама", "выручка"],
    },
]


# Функция: Генератор истории цен для графика
def generate_price_history(ticker, start_date_str, end_date_str):
    prices = []
    base_price = {"SBER": 280, "GAZP": 160, "YNDX": 2500}.get(ticker.upper(), 100)

    try:
        current_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)
    except ValueError:
        return []

    current_price = base_price

    while current_date <= end_date:
        if (
            current_date.weekday() < 5
        ):  # Только будние дни (Понедельник=0, Воскресенье=6)
            timestamp = int(current_date.timestamp() * 1000)
            prices.append([timestamp, round(current_price, 2)])
            current_price += current_price * random.uniform(-0.025, 0.025)
        current_date += timedelta(days=1)

    return prices


# ЭНДПОИНТ: для получения цен
@app.route("/get_ticker_prices", methods=["GET"])
def get_ticker_prices():
    ticker = request.args.get("ticker")
    date_start = request.args.get("date_start")
    date_end = request.args.get("date_end")

    if not all([ticker, date_start, date_end]):
        return (
            jsonify(
                {"error": "Missing required parameters: ticker, date_start, date_end"}
            ),
            400,
        )

    time.sleep(random.uniform(0.5, 1.0))
    price_data = generate_price_history(ticker, date_start, date_end)
    return jsonify(price_data)


# ЭНДПОИНТ: для получения новостей
@app.route("/get_ticker_news", methods=["GET"])
def get_ticker_news():
    time.sleep(random.uniform(0.2, 0.5))
    tickers_str = request.args.get("tickers")
    date_start_str = request.args.get("date_start")
    date_end_str = request.args.get("date_end")
    source_type = request.args.get("source_type")

    if not tickers_str:
        return jsonify([])

    tickers_list = tickers_str.upper().split(",")
    filtered_news = [news for news in mock_news if news["ticker"] in tickers_list]

    if date_start_str:
        try:
            date_start = datetime.fromisoformat(date_start_str + "T00:00:00")
            filtered_news = [
                n
                for n in filtered_news
                if datetime.fromisoformat(n["news_date"]) >= date_start
            ]
        except ValueError:
            pass

    if date_end_str:
        try:
            date_end = datetime.fromisoformat(date_end_str + "T23:59:59")
            filtered_news = [
                n
                for n in filtered_news
                if datetime.fromisoformat(n["news_date"]) <= date_end
            ]
        except ValueError:
            pass

    if source_type:
        filtered_news = [
            n for n in filtered_news if source_type.lower() in n["source"].lower()
        ]

    return jsonify(filtered_news)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
