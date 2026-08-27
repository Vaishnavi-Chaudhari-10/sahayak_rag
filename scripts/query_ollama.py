import ollama
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

collection_name = "legal_chunks"
query_text = "What are the packaging standards?"

# Encode query
query_vector = embedder.encode(query_text).tolist()

# Retrieve top-k chunks
search_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=3
)

# Build context
context = "\n".join([r.payload["text"] for r in search_results.points])

# Run query with Ollama
prompt = f"Answer the question using the context below:\n\n{context}\n\nQuestion: {query_text}\nAnswer:"
response = ollama.chat(model="qwen2.5:7b-instruct", messages=[
    {"role": "user", "content": prompt}
])

# print("🔎 Query:", query_text)
# print("\n📖 Answer:\n", response['message']['content'])


print("🔎 Query:", query_text)
print("\n📖 Raw Response:\n", response)

# Try to extract the answer safely
if "message" in response and "content" in response["message"]:
    print("\n📖 Answer:\n", response["message"]["content"])
elif "messages" in response and len(response["messages"]) > 0:
    print("\n📖 Answer:\n", response["messages"][0]["content"])
else:
    print("\n⚠️ Could not find answer content in response.")
