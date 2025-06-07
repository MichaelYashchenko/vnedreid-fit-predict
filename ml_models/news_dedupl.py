from typing import Callable, List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from natasha import Segmenter, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, Doc
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

class NewsDeduplicator:
    def __init__(self, embedding_fn: Callable[[str], np.ndarray], similarity_threshold: float = 0.85):
        """
        :param embedding_fn: Функция, возвращающая вектор np.ndarray по тексту.
        :param similarity_threshold: Порог для определения дубликатов.
        """
        self.embedding_fn = embedding_fn
        self.similarity_threshold = similarity_threshold
    def _are_similar(self, text1: str, text2: str) -> bool:
        vec1 = self.embedding_fn(text1).reshape(1, -1)
        vec2 = self.embedding_fn(text2).reshape(1, -1)
        sim = cosine_similarity(vec1, vec2)[0][0]
        return sim >= self.similarity_threshold
    def deduplicate(self, items: List[Dict]) -> List[Dict]:
        """
        :param items: Список словарей с ключом 'description' и другими полями
        :return: Список словарей с уникальными описаниями и числом удалённых дубликатов
        """
        result = []
        items = items['articles']
        used = [False] * len(items)
        for i, item_i in enumerate(items):
            if used[i]:
                continue
            group = [item_i]
            used[i] = True

            for j in range(i + 1, len(items)):
                if used[j]:
                    continue
                print(items)
                item_j = items[j]
                if self._are_similar(item_i['description'], item_j['description']):
                    used[j] = True
                    group.append(item_j)
            best_item = max(group, key=lambda x: len(x['description']))
            cleaned_item = best_item.copy()
            cleaned_item['duplicates_removed'] = len(group) - 1
            result.append(cleaned_item)
        return result
    @staticmethod
    def transformer_embed(text: str) -> np.ndarray:
        tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
        model = AutoModel.from_pretrained("cointegrated/rubert-tiny")
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
model = AutoModel.from_pretrained("cointegrated/rubert-tiny")

def transformer_embed(text: str) -> np.ndarray:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # Усреднение по токенам
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# from dedupl_class import NewsDeduplicator, transformer_embed
# import torch
#
# dedup = NewsDeduplicator(embedding_fn=transformer_embed, similarity_threshold=0.7)
# deduped_news = dedup.deduplicate(news)