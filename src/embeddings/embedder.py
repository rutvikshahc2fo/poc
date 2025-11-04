from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    def __init__(self, model_name: str = 'microsoft/codebert-base'):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list) -> np.ndarray:
        embs = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        norms[norms == 0] = 1e-9
        embs = embs / norms
        return embs.astype('float32')
