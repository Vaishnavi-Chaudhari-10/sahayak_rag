from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# Connect to Qdrant running locally
client = QdrantClient(host="localhost", port=6333)

# Load embedding model from HuggingFace
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Collection name
collection_name = "legal_chunks"

# If collection exists, delete it first
if client.collection_exists(collection_name):
    client.delete_collection(collection_name)

# Create collection with vector configuration
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(),
                                distance=Distance.COSINE)
)

# Example text chunks to embed
texts = [
    "Rule 24 — Labeling requirements for consumer goods.",
    "Rule 25 — Packaging standards for food products.",
    "Rule 26 — Safety standards for electrical appliances.",
    "Rule 27 — Environmental compliance for manufacturing units."
]

# Generate embeddings and prepare points
points = []
for idx, text in enumerate(texts):
    vector = model.encode(text).tolist()
    points.append(PointStruct(id=idx, vector=vector, payload={"text": text}))

# Upload points to Qdrant
client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"✅ Uploaded {len(points)} points to Qdrant collection '{collection_name}'")
