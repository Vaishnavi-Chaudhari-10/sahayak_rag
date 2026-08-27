from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Connect to LLM (OpenAI example)
llm = OpenAI()

collection_name = "legal_chunks"
query_text = "What are the packaging standards?"

# Step 1: Encode query
query_vector = model.encode(query_text).tolist()

# Step 2: Retrieve top-k chunks
search_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=3
)

# Step 3: Build context
context = "\n".join([r.payload["text"] for r in search_results.points])

# Step 4: Generate answer with LLM
prompt = f"Answer the question using the context below:\n\n{context}\n\nQuestion: {query_text}\nAnswer:"
response = llm.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

answer = response.choices[0].message.content

# Step 5: Attach citations
citations = []
for r in search_results.points:
    meta = r.payload
    citations.append(f"{meta.get('source','N/A')} | {meta.get('section','N/A')} | Page {meta.get('page','N/A')} | {meta.get('url','N/A')}")

print("🔎 Query:", query_text)
print("\n📖 Answer:\n", answer)
print("\n📚 Citations:\n", "\n".join(citations))
