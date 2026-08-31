# # import os
# # from pathlib import Path

# # from dotenv import load_dotenv
# # from pymongo import MongoClient


# # # ============================================================
# # # LOAD ENVIRONMENT VARIABLES
# # # ============================================================

# # # database.py is inside:
# # # sahayak/backend/database.py
# # #
# # # .env is inside:
# # # sahayak/.env
# # #
# # # Therefore:
# # # parent       -> backend
# # # parent.parent -> sahayak

# # BASE_DIR = Path(__file__).resolve().parent.parent

# # ENV_FILE = BASE_DIR / ".env"

# # load_dotenv(ENV_FILE)


# # # ============================================================
# # # GET ENVIRONMENT VARIABLES
# # # ============================================================

# # MONGODB_URL = os.getenv("MONGODB_URL")

# # DATABASE_NAME = os.getenv(
# #     "DATABASE_NAME",
# #     "sahayak"
# # )


# # # ============================================================
# # # CHECK MONGODB URL
# # # ============================================================

# # if not MONGODB_URL:
# #     raise ValueError(
# #         "MONGODB_URL is not set. "
# #         "Please check your .env file."
# #     )


# # # ============================================================
# # # MONGODB CONNECTION
# # # ============================================================

# # client = MongoClient(
# #     MONGODB_URL,
# #     serverSelectionTimeoutMS=5000
# # )


# # # ============================================================
# # # DATABASE
# # # ============================================================

# # db = client[DATABASE_NAME]


# # # ============================================================
# # # COLLECTIONS
# # # ============================================================

# # users_collection = db["users"]

# # chats_collection = db["chats"]


# # # ============================================================
# # # CREATE INDEX
# # # ============================================================

# # # Email must be unique.
# # # This prevents two accounts from using the same email.

# # users_collection.create_index(
# #     "email",
# #     unique=True
# # )


# # # ============================================================
# # # TEST CONNECTION
# # # ============================================================

# # def test_database():

# #     try:

# #         client.admin.command("ping")

# #         print(
# #             "MongoDB connection successful."
# #         )

# #         print(
# #             f"Database: {DATABASE_NAME}"
# #         )

# #     except Exception as e:

# #         print(
# #             "MongoDB connection failed:",
# #             e
# #         )


# # # ============================================================
# # # RUN TEST WHEN FILE IS EXECUTED DIRECTLY
# # # ============================================================

# # if __name__ == "__main__":

# #     test_database()


# import os
# from pathlib import Path

# from dotenv import load_dotenv
# from pymongo import MongoClient


# # ============================================================
# # LOAD .ENV FROM SAHAYAK ROOT
# # ============================================================

# BASE_DIR = Path(__file__).resolve().parent.parent

# ENV_FILE = BASE_DIR / ".env"

# load_dotenv(ENV_FILE)


# # ============================================================
# # ENVIRONMENT VARIABLES
# # ============================================================

# MONGODB_URL = os.getenv("MONGODB_URL")

# DATABASE_NAME = os.getenv(
#     "DATABASE_NAME",
#     "sahayak"
# )


# if not MONGODB_URL:
#     raise ValueError(
#         "MONGODB_URL is not set in the .env file."
#     )


# # ============================================================
# # MONGODB CONNECTION
# # ============================================================

# client = MongoClient(MONGODB_URL)

# db = client[DATABASE_NAME]


# # ============================================================
# # COLLECTIONS
# # ============================================================

# users_collection = db["users"]

# chats_collection = db["chats"]


# # ============================================================
# # CREATE INDEX
# # ============================================================

# users_collection.create_index(
#     "email",
#     unique=True
# )


# # ============================================================
# # TEST CONNECTION
# # ============================================================

# def test_database():

#     try:

#         client.admin.command("ping")

#         print("MongoDB connection successful.")

#     except Exception as e:

#         print(
#             "MongoDB connection failed:",
#             e
#         )


# # ============================================================
# # RUN TEST
# # ============================================================

# if __name__ == "__main__":

#     test_database()

# import os
# from pathlib import Path

# from dotenv import load_dotenv
# from pymongo import MongoClient


# # ============================================================
# # LOAD .ENV
# # ============================================================

# BASE_DIR = Path(__file__).resolve().parent.parent

# ENV_FILE = BASE_DIR / ".env"

# load_dotenv(ENV_FILE)


# # ============================================================
# # ENVIRONMENT VARIABLES
# # ============================================================

# MONGODB_URL = os.getenv("MONGODB_URL")

# DATABASE_NAME = os.getenv(
#     "DATABASE_NAME",
#     "sahayak"
# )


# # ============================================================
# # VALIDATE MONGODB URL
# # ============================================================

# if not MONGODB_URL:

#     raise RuntimeError(
#         "MONGODB_URL is missing from the .env file."
#     )


# # ============================================================
# # MONGODB CONNECTION
# # ============================================================

# try:

#     client = MongoClient(
#         MONGODB_URL,
#         serverSelectionTimeoutMS=5000
#     )

#     # Test connection immediately
#     client.admin.command("ping")

#     print(
#         "=================================================="
#     )

#     print(
#         "MongoDB connection successful."
#     )

#     print(
#         "Database:",
#         DATABASE_NAME
#     )

#     print(
#         "=================================================="
#     )

# except Exception as e:

#     print(
#         "=================================================="
#     )

#     print(
#         "MongoDB connection failed:",
#         e
#     )

#     print(
#         "=================================================="

#     )

#     raise RuntimeError(
#         "Could not connect to MongoDB."
#     )


# # ============================================================
# # DATABASE
# # ============================================================

# db = client[DATABASE_NAME]


# # ============================================================
# # COLLECTIONS
# # ============================================================

# users_collection = db["users"]

# chats_collection = db["chats"]


# # ============================================================
# # INDEXES
# # ============================================================

# # Email must be unique.
# #
# # This prevents duplicate accounts.

# try:

#     users_collection.create_index(
#         "email",
#         unique=True
#     )

# except Exception as e:

#     print(
#         "Could not create email index:",
#         e
#     )


# # ============================================================
# # CHAT INDEX
# # ============================================================

# try:

#     chats_collection.create_index(
#         [
#             ("user_id", 1),
#             ("created_at", -1)
#         ]
#     )

# except Exception as e:

#     print(
#         "Could not create chat index:",
#         e
#     )


# # ============================================================
# # DATABASE TEST FUNCTION
# # ============================================================

# def test_database():

#     try:

#         client.admin.command("ping")

#         print(
#             "MongoDB connection successful."
#         )

#         print(
#             f"Database: {DATABASE_NAME}"
#         )

#         return True

#     except Exception as e:

#         print(
#             "MongoDB connection failed:",
#             e
#         )

#         return False


# # ============================================================
# # RUN TEST
# # ============================================================

# if __name__ == "__main__":

#     test_database()
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient


# ============================================================
# LOAD .ENV
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

MONGODB_URL = os.getenv("MONGODB_URL")

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "sahayak"
)


# ============================================================
# VALIDATE MONGODB URL
# ============================================================

if not MONGODB_URL:

    raise RuntimeError(
        "MONGODB_URL is missing from the .env file."
    )


# ============================================================
# MONGODB CONNECTION
# ============================================================

try:

    client = MongoClient(
        MONGODB_URL,
        serverSelectionTimeoutMS=5000
    )

    # Force connection check
    client.admin.command("ping")

    print("==================================================")
    print("MongoDB connection successful.")
    print("Database:", DATABASE_NAME)
    print("==================================================")


except Exception as e:

    print("==================================================")
    print("MongoDB connection failed:")
    print(e)
    print("==================================================")

    raise RuntimeError(
        "Could not connect to MongoDB."
    )


# ============================================================
# DATABASE
# ============================================================

db = client[DATABASE_NAME]


# ============================================================
# COLLECTIONS
# ============================================================

users_collection = db["users"]

chats_collection = db["chats"]


# ============================================================
# INDEXES
# ============================================================

# Email must be unique.

try:

    users_collection.create_index(
        "email",
        unique=True
    )

except Exception as e:

    print(
        "Warning: Could not create email index:",
        e
    )


# ============================================================
# TEST DATABASE
# ============================================================

def test_database():

    try:

        client.admin.command("ping")

        print(
            "MongoDB connection successful."
        )

        print(
            f"Database: {DATABASE_NAME}"
        )

        return True

    except Exception as e:

        print(
            "MongoDB connection failed:",
            e
        )

        return False


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    test_database()