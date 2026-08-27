from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

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

# Load quantized LLaMA model
llm = Llama(model_path="models/llama-2-7b-chat.Q4_K_M.gguf")

# Generate answer
prompt = f"Answer the question using the context below:\n\n{context}\n\nQuestion: {query_text}\nAnswer:"
response = llm(prompt, max_tokens=256)

print("🔎 Query:", query_text)
print("\n📖 Answer:\n", response["choices"][0]["text"])
