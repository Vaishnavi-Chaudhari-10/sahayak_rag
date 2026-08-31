import os

from dotenv import load_dotenv

from qdrant_client import QdrantClient, models


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

# load_dotenv()
# load_dotenv("../.env")

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ENV_PATH = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(ENV_PATH)

print("Loading .env from:", ENV_PATH)

LOCAL_QDRANT_URL = os.getenv(
    "LOCAL_QDRANT_URL",
    "http://localhost:6333"
)

CLOUD_QDRANT_URL = os.getenv(
    "CLOUD_QDRANT_URL"
)

CLOUD_QDRANT_API_KEY = os.getenv(
    "CLOUD_QDRANT_API_KEY"
)

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "ayurveda_ip"
)

# LOCAL_QDRANT_URL = os.getenv(
#     "LOCAL_QDRANT_URL",
#     "http://localhost:6333"
# )

# CLOUD_QDRANT_URL = os.getenv(
#     "https://4d8a63ec-0933-4ace-aa8d-b4b6d626ae6d.sa-east-1-0.aws.cloud.qdrant.io"
# )

# CLOUD_QDRANT_API_KEY = os.getenv(
#     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6ZmE2NzNmMzYtOTc2Zi00MmQzLWE5NWQtYTZiMjc3Y2IyNTljIn0.ex0TgiYNhhFrHLTb7a_SoYMRr8RdXWvuUTTn6NcQnOY"
# )

# COLLECTION_NAME = os.getenv(
#     "COLLECTION_NAME",
#     "ayurveda_ip"
# )


# ============================================================
# VALIDATE CONFIGURATION
# ============================================================

if not CLOUD_QDRANT_URL:
    raise ValueError(
        "CLOUD_QDRANT_URL is missing from .env"
    )

if not CLOUD_QDRANT_API_KEY:
    raise ValueError(
        "CLOUD_QDRANT_API_KEY is missing from .env"
    )


# ============================================================
# CONNECT TO LOCAL QDRANT
# ============================================================

print("\nConnecting to local Qdrant...")

local_client = QdrantClient(
    url="http://localhost:6333"
)

print("Connected to local Qdrant.")


# ============================================================
# CONNECT TO QDRANT CLOUD
# ============================================================

print("\nConnecting to Qdrant Cloud...")

cloud_client = QdrantClient(
    url="https://4d8a63ec-0933-4ace-aa8d-b4b6d626ae6d.sa-east-1-0.aws.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6ZmE2NzNmMzYtOTc2Zi00MmQzLWE5NWQtYTZiMjc3Y2IyNTljIn0.ex0TgiYNhhFrHLTb7a_SoYMRr8RdXWvuUTTn6NcQnOY"
)

print("Connected to Qdrant Cloud.")


# ============================================================
# CHECK LOCAL COLLECTION
# ============================================================

print(
    f"\nChecking local collection: {COLLECTION_NAME}"
)

local_info = local_client.get_collection(
    collection_name=COLLECTION_NAME
)

print(
    "Local collection information:"
)

print(
    local_info
)


# ============================================================
# GET VECTOR CONFIGURATION
# ============================================================

vectors_config = (
    local_info.config.params.vectors
)

print(
    "\nLocal vector configuration:"
)

print(
    vectors_config
)


# ============================================================
# CREATE CLOUD COLLECTION
# ============================================================

print(
    f"\nChecking cloud collection: {COLLECTION_NAME}"
)

cloud_collections = (
    cloud_client.get_collections()
)

cloud_collection_names = [

    collection.name

    for collection
    in cloud_collections.collections

]


if COLLECTION_NAME in cloud_collection_names:

    print(
        f"Collection '{COLLECTION_NAME}' "
        "already exists in Qdrant Cloud."
    )

else:

    print(
        f"Creating '{COLLECTION_NAME}' "
        "in Qdrant Cloud..."
    )

    # Your screenshot shows:
    # 384 dimensions
    # Cosine distance

    cloud_client.create_collection(

        collection_name=COLLECTION_NAME,

        vectors_config=models.VectorParams(

            size=384,

            distance=models.Distance.COSINE

        )

    )

    print(
        "Cloud collection created successfully."
    )


# ============================================================
# COPY POINTS
# ============================================================

print(
    "\nStarting migration..."
)

batch_size = 100

offset = None

total_migrated = 0


while True:

    records, next_offset = local_client.scroll(

        collection_name=COLLECTION_NAME,

        limit=batch_size,

        offset=offset,

        with_payload=True,

        with_vectors=True

    )


    if not records:

        break


    points = []


    for record in records:

        points.append(

            models.PointStruct(

                id=record.id,

                vector=record.vector,

                payload=record.payload

            )

        )


    cloud_client.upsert(

        collection_name=COLLECTION_NAME,

        points=points,

        wait=True

    )


    total_migrated += len(points)


    print(
        f"Migrated {total_migrated} points..."
    )


    if next_offset is None:

        break


    offset = next_offset


# ============================================================
# VERIFY MIGRATION
# ============================================================

print(
    "\nMigration completed."
)

print(
    f"Total points migrated: {total_migrated}"
)


cloud_info = cloud_client.get_collection(

    collection_name=COLLECTION_NAME

)


print(
    "\nCloud collection information:"
)

print(
    cloud_info
)


print(
    "\n===================================="
)

print(
    "QDRANT MIGRATION SUCCESSFUL"
)

print(
    "===================================="
)

print(
    f"Collection: {COLLECTION_NAME}"
)

print(
    f"Points migrated: {total_migrated}"
)

print(
    "====================================\n"
)