from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc,
    MorphVocab,
)
import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_ner(text: str):
    # 1. Инициализация компонентов
    segmenter     = Segmenter()
    embedding     = NewsEmbedding()
    morph_tagger  = NewsMorphTagger(embedding)
    syntax_parser = NewsSyntaxParser(embedding)
    ner_tagger    = NewsNERTagger(embedding)
    morph_vocab   = MorphVocab()

    # 2. Создаём объект Doc и запускаем пайплайн
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    # 3. Нормализация и сбор сущностей
    entities = []
    for span in doc.spans:
        span.normalize(morph_vocab)
        entities.append({
            "text":       span.text,
            "normalized": span.normal,
            "type":       span.type  # PER, ORG, LOC, etc.
        })
    return entities

def normalize_entities(entities):
    # Сортируем по длине (от длинных к коротким)
    sorted_entities = sorted(entities, key=len, reverse=True)
    unique_entities = []

    for ent in sorted_entities:
        # Если текущая сущность не содержится ни в одной из уже добавленных
        if not any(ent in existing_ent for existing_ent in unique_entities):
            unique_entities.append(ent)

    return unique_entities


def get_result(text, topk=5):

    ner_results = extract_ner(text)
    ner_names = [d['normalized'] for d in ner_results]
    unique_entities = normalize_entities(ner_names)

    vectorizer = TfidfVectorizer(
        lowercase=False,
        use_idf=False,      # отключаем IDF
    )
    X = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    tf_weights = {tok: X[0, idx] for idx, tok in enumerate(feature_names)}

    entity_weights = {}
    for ent in unique_entities:
        w = sum(tf_weights.get(tok, 0.0) for tok in ent.split())
        temp_weight = entity_weights.get(ent, 0.0) + w
        if temp_weight > 0:
            entity_weights[ent] = temp_weight

    return [i for i, j in sorted(entity_weights.items(), key=lambda x: x[1], reverse=True)[:topk]]

def ner_news(news):
    for new_ind in range(0, len(news)):
        news[new_ind]['key_words'] = get_result(news[new_ind]['news_summary'])
    return news