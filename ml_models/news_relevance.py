# Инициализация пайплайна
from sklearn.metrics import accuracy_score, classification_report
from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="clapAI/roberta-large-multilingual-sentiment",
    tokenizer="clapAI/roberta-large-multilingual-sentiment",
    device=-1  # или -1 для CPU
)

def get_news_relevance(news):
    for new_i in range(0, len(news)):
        result = sentiment_pipeline(news[new_i]['description'])
        news[new_i]['news_sentiment'] = result[0]['label']
        news[new_i]['news_sentiment_score'] = result[0]['score']
    return news
