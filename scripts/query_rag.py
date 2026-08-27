from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

# Load model + index
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
index = faiss.read_index("vector_index.faiss")
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

def search(query, k=5):
    query_vec = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vec, k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        results.append({
            "text": metadata[idx]["chunk_id"],
            "source_id": metadata[idx]["source_id"],
            "section": metadata[idx]["section"],
            "page": metadata[idx]["page"],
            "distance": float(dist)
        })
    return results

# Example query
results = search("Ayurveda labeling requirements")
for r in results:
    print(r)
