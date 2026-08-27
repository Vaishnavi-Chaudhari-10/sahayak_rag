from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Load the same embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Collection name
collection_name = "legal_chunks"

# Example query
query_text = "What are the packaging standards?"

# Encode query
query_vector = model.encode(query_text).tolist()

# Perform search (modern method)
search_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=3  # top 3 results
)

# Print results
print(f"🔎 Query: {query_text}\n")
for result in search_results.points:
    print(f"Score: {result.score:.4f} | Text: {result.payload['text']}")
