from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

collection_name = "legal_chunks"

# Reset collection
if client.collection_exists(collection_name):
    client.delete_collection(collection_name)

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=model.get_embedding_dimension(),
                                distance=Distance.COSINE)
)

# Read PDF
reader = PdfReader("ConsumerLaw.pdf")  # place your PDF in the project folder
points = []
chunk_id = 0

for page_num, page in enumerate(reader.pages, start=1):
    text = page.extract_text()
    if text:
        # Split into smaller chunks (e.g., paragraphs)
        for para in text.split("\n"):
            para = para.strip()
            if para:
                vector = model.encode(para).tolist()
                points.append(PointStruct(
                    id=chunk_id,
                    vector=vector,
                    payload={
                        "text": para,
                        "source": "ConsumerLaw.pdf",
                        "page": page_num
                    }
                ))
                chunk_id += 1

# Upload to Qdrant
client.upsert(collection_name=collection_name, points=points)
print(f"✅ Uploaded {len(points)} chunks from PDF into Qdrant")
