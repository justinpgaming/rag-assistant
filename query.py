import numpy as np
from sentence_transformers import SentenceTransformer
import json

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load embeddings + chunks
embeddings = np.load("embeddings.npy")

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query, top_k=5):
    query_embedding = model.encode(query)

    scores = []
    for i, emb in enumerate(embeddings):
        score = cosine_similarity(query_embedding, emb)
        scores.append((score, i))

    # Sort by best match
    scores.sort(reverse=True, key=lambda x: x[0])

    results = []
    for score, idx in scores[:top_k]:
        results.append({
            "score": float(score),
            "text": chunks[idx]
        })

    return results


if __name__ == "__main__":
    while True:
        query = input("\nAsk something (or 'exit'): ")
        if query.lower() == "exit":
            break

        results = search(query)

        print("\nTop Results:\n")
        for r in results:
            print(f"Score: {r['score']:.4f}")
            print(r["text"])
            print("-" * 50)
