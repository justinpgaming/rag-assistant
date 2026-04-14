import numpy as np
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_data():
    embeddings = np.load("embeddings.npy")

    with open("chunks.json", "r", encoding="utf-8") as f:
        texts = json.load(f)

    database = []
    for i in range(len(texts)):
        database.append({
            "content": texts[i],
            "embedding": embeddings[i]
        })

    return database


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query, database, top_k=5):
    q_emb = model.encode(query)

    scores = []
    for c in database:
        score = cosine_similarity(q_emb, c["embedding"])
        scores.append((score, c))

    scores.sort(key=lambda x: x[0], reverse=True)

    return [c for _, c in scores[:top_k]]
