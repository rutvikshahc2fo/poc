from ingestion.file_loader import list_py_files
from parsing.python_parser import extract_functions_from_file
from embeddings.embedder import Embedder
from storage.faiss_store import FaissStore


from typing import List, Dict
import numpy as np


class DuplicateDetector:
    def __init__(self, threshold: float = 0.9, top_k: int = 5, model_name: str = 'microsoft/codebert-base'):
        self.threshold = threshold
        self.top_k = top_k
        self.embedder = Embedder(model_name=model_name)
        self.store = None


    def run(self, path: str) -> List[Dict]:
        files = list_py_files(path)
        all_chunks = []
        for f in files:
            chunks = extract_functions_from_file(str(f))
            all_chunks.extend(chunks)

        if not all_chunks:
            return []

        texts = [c.source for c in all_chunks]
        embs = self.embedder.embed(texts)


        dim = embs.shape[1]
        self.store = FaissStore(dim=dim)


        metadatas = [c.to_dict() for c in all_chunks]
        self.store.add(embs, metadatas)

        duplicates = []

        for i, vec in enumerate(embs):
            results = self.store.search(vec, self.top_k + 1)
            for score, meta, idx in results:

                if idx == i:
                    continue
                if score >= self.threshold:
                    a = metadatas[i]
                    b = meta
                    key = tuple(sorted([f"{a['file_path']}:{a['start_lineno']}", f"{b['file_path']}:{b['start_lineno']}"]))
                    duplicates.append({
                        'a_file': a['file_path'],
                        'a_name': a['name'],
                        'a_start': a['start_lineno'],
                        'b_file': b['file_path'],
                        'b_name': b['name'],
                        'b_start': b['start_lineno'],
                        'score': score,
                        'key': key,
                    })

        dedup_map = {}
        for d in duplicates:
            k = d['key']
            if k not in dedup_map or d['score'] > dedup_map[k]['score']:
                dedup_map[k] = d


        final = sorted(list(dedup_map.values()), key=lambda x: x['score'], reverse=True)
        for r in final:
            r.pop('key', None)
        return final