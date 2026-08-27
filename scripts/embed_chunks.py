from sentence_transformers import SentenceTransformer
import faiss
import json
from pathlib import Path
import numpy as np

CHUNKS_DIR = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\chunks_legal")
INDEX_PATH = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\vector_index.faiss")

# Load multilingual model
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Collect all chunks
texts, metadata = [], []
for chunk_file in CHUNKS_DIR.rglob("*.json"):
    with open(chunk_file, "r", encoding="utf-8") as f:
        chunk = json.load(f)
        texts.append(chunk["text"])
        metadata.append({
            "chunk_id": chunk["chunk_id"],
            "source_id": chunk["source_id"],
            "section": chunk["section"],
            "page": chunk["page"]
        })

# Generate embeddings
embeddings = model.encode(texts, convert_to_numpy=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index + metadata
faiss.write_index(index, str(INDEX_PATH))
with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print(f"✅ Stored {len(texts)} chunks in FAISS index")
