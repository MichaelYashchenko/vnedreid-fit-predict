from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch

class NewsDeduplicatorFast:
    def __init__(self, tokenizer, model, similarity_threshold: float = 0.85, device=None):
        self.similarity_threshold = similarity_threshold
        self.tokenizer = tokenizer
        self.model = model
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        inputs = self.tokenizer(
            texts, return_tensors="pt", padding=True, truncation=True, max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        return embeddings

    def deduplicate(self, items: List[Dict]) -> List[Dict]:
        print(items)
        descriptions = [item['news_summary'] for item in items]
        embeddings = self.embed_batch(descriptions)

        similarity_matrix = cosine_similarity(embeddings)
        n = len(items)
        used = [False] * n
        result = []

        for i in range(n):
            if used[i]:
                continue
            group = [i]
            used[i] = True
            for j in range(i + 1, n):
                if not used[j] and similarity_matrix[i, j] >= self.similarity_threshold:
                    group.append(j)
                    used[j] = True

            best_idx = max(group, key=lambda idx: len(items[idx]['news_summary']))
            item = items[best_idx].copy()
            item['duplicates'] = len(group) - 1
            result.append(item)

        return result

from transformers import AutoTokenizer, AutoModel

def deduplicate_news(news):
    tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
    model = AutoModel.from_pretrained("cointegrated/rubert-tiny")
    deduplicator = NewsDeduplicatorFast(tokenizer=tokenizer, model=model)
    unique_news = deduplicator.deduplicate(news)
    return unique_news
