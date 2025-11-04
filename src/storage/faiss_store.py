import faiss
import numpy as np


class FaissStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, vectors: np.ndarray, metadatas: list):
        assert vectors.shape[1] == self.dim
        self.index.add(vectors)
        self.metadata.extend(metadatas)

    def search(self, vector: np.ndarray, k: int):

        if vector.ndim == 1:
            vector = vector.reshape(1, -1)
        D, I = self.index.search(vector, k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            results.append((float(score), self.metadata[idx], idx))
        return results

    def ntotal(self):
        return self.index.ntotal
