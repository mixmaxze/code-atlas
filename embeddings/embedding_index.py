from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

class CodeEmbeddingIndex:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.chunks = []

    def build_index(self, chunks):

        texts = [chunk["code"] for chunk in chunks]

        embeddings = self.model.encode(texts)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(np.array(embeddings))

        self.chunks = chunks

    def search(self, query, k=5):

        query_embedding = self.model.encode([query])

        distances, indices = self.index.search(
            np.array(query_embedding),
            k
        )

        results = []

        for idx in indices[0]:
            results.append(self.chunks[idx])

        return results
    
    def save(self, path):

        with open(path, "wb") as f:
            pickle.dump({
                "index": self.index,
                "chunks": self.chunks
            }, f)

    def load(self, path):

        with open(path, "rb") as f:

            data = pickle.load(f)

            self.index = data["index"]

            self.chunks = data["chunks"]
