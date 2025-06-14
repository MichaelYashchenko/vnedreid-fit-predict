from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news_router# , portfolio_router
import uvicorn
import redis
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
# from app.models.database import engine, Base
env_file_path = "../.env"
load_dotenv(env_file_path)
# # Читаем переменные
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
# # Инициализация базы (создание таблиц, если нужно)
# # Base.metadata.create_all(bind=engine)
#
app = FastAPI(docs_url="/", title="News Aggregator Service")

# Configure Redis (optional)
redis_client = redis.Redis(host="localhost", port=6379, db=0)
FastAPICache.init(RedisBackend(redis_client), prefix="cache")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#
app.include_router(news_router.router, prefix="/news", tags=["news"])
# app.include_router(portfolio_router.router, prefix="/portfolio", tags=["portfolio"])


uvicorn.run(app)




# from .services.news_service import NewsService
# from datetime import datetime, timedelta, timezone
# from ml_models.news_dedupl import NewsDeduplicator, transformer_embed
# import torch
#
# from_date = datetime(2025,5,7)
# to_date = datetime(2025,6,7)
# news_service = NewsService(NEWS_API_KEY)
# news = {'totalArticles': 18, 'articles': [{'title': 'Курс рубля, цены на нефть и рынок акций со 2 по 8 июня 2025: прогнозы', 'description': 'Финансовые аналитики прогнозируют, что будет с фондовым рынком, курсом рубля и стоимостью нефти на следующей неделе со 2 по 8 июня 2025.', 'content': 'Рубль\nМихаил Васильев, главный аналитик Совкомбанка:\n"Мы полагаем, что на предстоящей неделе рубль останется крепким и будет торговаться в диапазоне 10,6-11,3 руб. за юань, 76-81 руб. за долл., 86-92 руб. за евро.\nВалютный рынок продолжит чутко реаги... [4316 chars]', 'url': 'https://rg.ru/2025/05/31/chto-budet-s-rublem-neftiu-i-birzhej-na-nedele-so-2-po-8-iiunia.html', 'image': 'https://cdnstatic.rg.ru/uploads/images/2025/05/30/img_4254-kopiya_da7_028.jpg', 'publishedAt': '2025-05-30T21:00:00Z', 'source': {'name': 'Российская Газета', 'url': 'https://rg.ru'}}, {'title': 'Жительница дома на улице Генерала Тюленева, где взорвался газ, описала, как выглядят квартиры', 'description': 'Продолжаются мучения жителей дома на улице Генерала Тюленева, где 4 мая взорвался газ.\nЭпицентром взрыва стала квартира на 9 этаже в 12 подъезде.\nНа этой неделе жильцы зашли в квартиры и ужаснулись.', 'content': '— Меня пригласили на этой неделе, мол, приходите, посмотрите, какой ремонт вам сделали, если все устраивает, заносите вещи, - рассказывает жительница одного из нижних этажей. — Квартиры в нашем подъезде все пострадали, водой залило до первого этажа. ... [1590 chars]', 'url': 'https://www.mk.ru/social/2025/05/30/zhitelnica-doma-na-ulice-generala-tyuleneva-gde-vzorvalsya-gaz-opisala-kak-vyglyadyat-kvartiry.html', 'image': 'https://static.mk.ru/upload/entities/2025/05/30/18/articles/facebookPicture/65/7a/f0/3a/e1c83f5c5c182d4c57ff76cf7884f0c3.jpg', 'publishedAt': '2025-05-30T15:34:02Z', 'source': {'name': 'Московский Комсомолец', 'url': 'https://www.mk.ru'}}, {'title': '"Газпром" поставил в Китай 100 млрд кубометром газа по "Силе Сибири"', 'description': 'Объем поставленного «Газпромом» (MOEX: GAZP) топлива в Китай по газопроводу «Сила Сибири» достиг 100 млрд кубометров. Об этом сообщил глава холдинга Алексей Миллер.', 'content': 'Объем поставленного «Газпромом» (MOEX: GAZP) топлива в Китай по газопроводу «Сила Сибири» достиг 100 млрд кубометров. Об этом сообщил глава холдинга Алексей Миллер.\nВыйти из полноэкранного режима Развернуть на весь экран Фото: Эмин Джафаров, Коммерса... [792 chars]', 'url': 'https://www.kommersant.ru/doc/7772779', 'image': 'https://iv.kommersant.ru/SocialPics/7772779_49_2822655_547870764', 'publishedAt': '2025-05-30T11:02:19Z', 'source': {'name': 'Коммерсантъ', 'url': 'https://www.kommersant.ru'}}, {'title': 'Три угрозы Трампа для России', 'description': 'Обсуждаются варианты снижения потолка цен на нефть, введения вторичных санкций и конфискации замороженных активов ЦБ РФ. Росбалт', 'content': 'Контекст. 5 декабря 2022 года вступило в силу эмбарго на поставку российской нефти по морю в Евросоюз. Одновременно с этим ЕС, страны G7, ЕС и Австралия ввели регулируемый потолок цен на российскую нефть, поставляемую по морю, на уровне $60 за баррел... [443 chars]', 'url': 'https://www.rosbalt.ru/news/2025-05-28/tri-ugrozy-trampa-dlya-rossii-5400289', 'image': 'https://files.1mi.media/c59652c00560608c30e92381b5d368002daf9d66/c:1920:1080:nowe:0:0/fcd964e8d41c3bbe66114c1fb6c187140e671942b611c184be90f3e05eeb.jpg', 'publishedAt': '2025-05-27T21:00:00Z', 'source': {'name': 'Росбалт', 'url': 'https://www.rosbalt.ru'}}, {'title': 'FT: ЕК настаивает на снижении потолка цен на нефть из России', 'description': 'FT: ЕК\xa0настаивает на\xa0снижении потолка цен на\xa0нефть из\xa0России - Читайте подробнее на сайте РТ на русском.', 'content': 'Еврокомиссия предлагает ужесточить антироссийские санкции, снизив потолок цен на нефть из России с $60 до $45 за баррель, пишет газета Financial Times со ссылкой на источники.\nПо информации источников, данная инициатива рассматривается в рамках 18-го... [721 chars]', 'url': 'https://russian.rt.com/business/news/1483966-potolok-cen-neft-rossiya', 'image': 'https://russian.rt.com/static/blocks/og-img/pl-17.jpg', 'publishedAt': '2025-05-27T06:30:00Z', 'source': {'name': 'RT на русском', 'url': 'https://russian.rt.com'}}, {'title': 'Литовская компания продолжает закупать российский аммиак из-за газового кризиса', 'description': 'Литовская компания Achemа, ранее остановившая производство аммиака из-за высоких цен на газ, была вынуждена закупать его у российских поставщиков для выполнения контрактных обязательств.', 'content': 'Литовская компания Achemа, ранее остановившая производство аммиака из-за высоких цен на газ, была вынуждена закупать его у российских поставщиков для выполнения контрактных обязательств.\nКак сообщает издание LRT со ссылкой на представителя компании Й... [503 chars]', 'url': 'https://www.mk.ru/politics/2025/05/27/litovskaya-kompaniya-prodolzhaet-zakupat-rossiyskiy-ammiak-izza-gazovogo-krizisa.html', 'image': 'https://static.mk.ru/upload/entities/2025/05/27/00/articles/facebookPicture/a9/19/71/65/2af1c6a484375de77aa653d282fdfcf2.jpg', 'publishedAt': '2025-05-26T21:17:39Z', 'source': {'name': 'Московский Комсомолец', 'url': 'https://www.mk.ru'}}, {'title': 'Курс рубля, цены на нефть и рынок акций с 26 мая по 1 июня 2025: прогнозы', 'description': 'Финансовые аналитики прогнозируют, что будет с фондовым рынком, курсом рубля и стоимостью нефти на следующей неделе с 26 мая по 1 июня 2025.', 'content': 'Рубль\nМихаил Васильев, главный аналитик "Совкомбанка":\n- Мы полагаем, что на предстоящей неделе рубль останется крепким и будет торговаться в диапазоне 10,6-11,4 руб. за юань, 76-82 руб. за долл., 86-93 руб. за евро.\nВалютный рынок продолжит чутко ре... [4430 chars]', 'url': 'https://rg.ru/2025/05/23/chto-budet-s-rublem-neftiu-i-birzhej-na-nedele-s-26-maia-po-1-iiunia.html', 'image': 'https://cdnstatic.rg.ru/uploads/images/2025/05/23/img_4203-kopiya_dcb_bea.jpg', 'publishedAt': '2025-05-22T21:00:00Z', 'source': {'name': 'Российская Газета', 'url': 'https://rg.ru'}}, {'title': 'ЕС захотел снизить потолок цен на нефть из России, пишет Reuters', 'description': 'Евросоюз призовет страны G7 снизить потолок цены на российскую нефть, доставляемую по морю, передает агентство Reuters со ссылкой на чиновников. РИА Новости, 19.05.2025', 'content': 'https://ria.ru/20250519/neft-2017851921.html\nЕС захотел снизить потолок цен на нефть из России, пишет Reuters\nЕС захотел снизить потолок цен на нефть из России, пишет Reuters - РИА Новости, 19.05.2025\nЕС захотел снизить потолок цен на нефть из России... [2456 chars]', 'url': 'https://ria.ru/20250519/neft-2017851921.html', 'image': 'https://cdnn21.img.ria.ru/images/sharing/article/2017851921.jpg?15246658591747659100', 'publishedAt': '2025-05-19T12:22:00Z', 'source': {'name': 'РИА НОВОСТИ', 'url': 'https://ria.ru'}}, {'title': '"Газпром" подготовит долгосрочный контракт с европейской страной', 'description': 'В настоящее время «Газпром» готовит новый долгосрочный контракт на поставки газа по трубопроводу с Сербией, соответствующие поручения даны. Об этом заявил вице-премьер России Александр Новак, передает ТАСС', 'content': 'Вице-премьер Новак заявил о подготовке нового контракта «Газпрома» с Сербией\nВ настоящее время «Газпром» готовит новый долгосрочный контракт на поставки газа по трубопроводу с Сербией, соответствующие поручения даны. Об этом заявил вице-премьер Росси... [771 chars]', 'url': 'https://lenta.ru/news/2025/05/19/gazprom-for-bratushki/', 'image': 'https://icdn.lenta.ru/images/2025/05/19/21/20250519210016279/share_f38572561bb2a6556eaf17f350777516.jpg', 'publishedAt': '2025-05-18T21:00:00Z', 'source': {'name': 'Lenta.ru', 'url': 'https://lenta.ru'}}, {'title': 'Суд обратил в доход государства имущество бывшего главы "Газпром энерго"', 'description': 'Суд обратил в доход государства имущество бывшего главы «Газпром энерго» - Читайте подробнее на сайте РТ на русском.', 'content': 'Фрунзенский суд Санкт-Петербурга удовлетворил иск Генпрокуратуры России к бывшему генеральному директору компании «Газпром энерго» Алексею Митюшову, его двум родственникам, бизнес-партнёру Юлии Симаковой и нескольким другим ответчикам.\n«Решение подле... [827 chars]', 'url': 'https://russian.rt.com/russia/news/1479162-sud-imuschestvo-gazprom-energo', 'image': 'https://russian.rt.com/static/blocks/og-img/pl-17.jpg', 'publishedAt': '2025-05-16T20:14:00Z', 'source': {'name': 'RT на русском', 'url': 'https://russian.rt.com'}}]}
#
# dedup = NewsDeduplicator(embedding_fn=transformer_embed, similarity_threshold=0.7)
# deduped_news = dedup.deduplicate(news)
# print(deduped_news)
# deduped_news = dedup.deduplicate(news)
# print(deduped_news)