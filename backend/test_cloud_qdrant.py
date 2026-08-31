import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

print("Connecting to Qdrant Cloud...")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

info = client.get_collection(
    collection_name=QDRANT_COLLECTION
)

print("\nConnected successfully!")
print("Collection:", QDRANT_COLLECTION)
print("Points:", info.points_count)
print("Vector size:", info.config.params.vectors.size)
print("Distance:", info.config.params.vectors.distance)