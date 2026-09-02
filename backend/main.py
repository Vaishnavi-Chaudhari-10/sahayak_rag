
import os
from datetime import datetime, timezone

import requests
from bson import ObjectId
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from auth import (
    router as auth_router,
    get_current_user
)

from database import chats_collection


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# ENVIRONMENT SETTINGS
# ============================================================

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)


# ============================================================
# QDRANT CLOUD
# ============================================================

QDRANT_URL = os.getenv(
    "CLOUD_QDRANT_URL",
    ""
)

QDRANT_API_KEY = os.getenv(
    "CLOUD_QDRANT_API_KEY",
    ""
)

QDRANT_COLLECTION = os.getenv(
    "QDRANT_COLLECTION",
    "ayurveda_ip"
)


# ============================================================
# RAG SETTINGS
# ============================================================

RAG_SCORE_THRESHOLD = float(
    os.getenv(
        "RAG_SCORE_THRESHOLD",
        "0.45"
    )
)

TOP_K = int(
    os.getenv(
        "RAG_TOP_K",
        "5"
    )
)


# ============================================================
# GEMINI
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Sahayak API",
    description=(
        "AI Assistant for Ayurveda IP & Regulation"
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

allowed_origins = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

allowed_origins = list(
    dict.fromkeys(
        origin.rstrip("/")
        for origin in allowed_origins
        if origin
    )
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# AUTH
# ============================================================

app.include_router(
    auth_router
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QueryRequest(BaseModel):

    query: str

    language: str = "English"

    stakeholder: str = "Researcher"


# ============================================================
# QDRANT INITIALIZATION
# ============================================================

qdrant = None


if QDRANT_URL and QDRANT_API_KEY:

    try:

        qdrant = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            check_compatibility=False
        )

        print(
            "=================================================="
        )

        print(
            "QDRANT: Connected to Qdrant Cloud"
        )

        print(
            "Collection:",
            QDRANT_COLLECTION
        )

        # Verify collection
        collections = qdrant.get_collections()

        collection_names = [
            c.name
            for c in collections.collections
        ]

        if QDRANT_COLLECTION not in collection_names:

            print(
                "WARNING: Collection not found:",
                QDRANT_COLLECTION
            )

        else:

            print(
                "QDRANT COLLECTION VERIFIED:",
                QDRANT_COLLECTION
            )

        print(
            "=================================================="
        )

    except Exception as e:

        print(
            "QDRANT INITIALIZATION ERROR:",
            e
        )

        qdrant = None

else:

    print(
        "=================================================="
    )

    print(
        "QDRANT: Not configured"
    )

    print(
        "=================================================="
    )


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedder = None


def get_embedder():

    global embedder

    if embedder is None:

        print("========================================")
        print("Loading embedding model...")
        print("Model: all-MiniLM-L6-v2")
        print("========================================")

        try:

            embedder = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

            print(
                "Embedding model loaded successfully."
            )

            print(
                "Embedding dimension:",
                embedder.get_sentence_embedding_dimension()
            )

        except Exception as e:

            print(
                "EMBEDDING MODEL ERROR:",
                repr(e)
            )

            embedder = None

            raise

    return embedder
# ============================================================
# GEMINI CONFIGURATION
# ============================================================

if GEMINI_API_KEY:

    print(
        "=================================================="
    )

    print(
        "GEMINI: Configured"
    )

    print(
        "Model:",
        GEMINI_MODEL
    )

    print(
        "=================================================="
    )

else:

    print(
        "=================================================="
    )

    print(
        "GEMINI: NOT CONFIGURED"
    )

    print(
        "=================================================="
    )


# ============================================================
# GEMINI ANSWER GENERATION
# ============================================================

def generate_answer(prompt: str) -> str:

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )


    headers = {

        "x-goog-api-key":
            GEMINI_API_KEY,

        "Content-Type":
            "application/json"
    }


    payload = {

        "contents": [

            {

                "parts": [

                    {

                        "text":
                            prompt
                    }

                ]

            }

        ],

        "generationConfig": {

            "temperature":
                0.2
        }

    }


    print(
        "Generating answer with Gemini:",
        GEMINI_MODEL
    )


    response = requests.post(

        GEMINI_URL,

        headers=headers,

        json=payload,

        timeout=120
    )


    print(
        "Gemini HTTP status:",
        response.status_code
    )


    if not response.ok:

        print(
            "Gemini response:",
            response.text
        )

        raise RuntimeError(
            "Gemini API returned an error."
        )


    data = response.json()


    try:

        answer = (

            data[
                "candidates"
            ][
                0
            ][
                "content"
            ][
                "parts"
            ][
                0
            ][
                "text"
            ]

        )

    except (
        KeyError,
        IndexError,
        TypeError
    ):

        print(
            "Unexpected Gemini response:",
            data
        )

        raise RuntimeError(
            "Unexpected Gemini response format."
        )


    if not answer:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return answer.strip()


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {

        "message":
            "Sahayak backend is running",

        "status":
            "online",

        "service":
            "Sahayak API",

        "version":
            "1.0.0",

        "llm":
            GEMINI_MODEL
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {

        "status":
            "healthy",

        "qdrant":
            (
                "connected"
                if qdrant is not None
                else "not_configured"
            ),

        "collection":
            QDRANT_COLLECTION,

        "embedding_model":
            (
                "loaded"
                if embedder is not None
                else "unavailable"
            ),

        "gemini":
            (
                GEMINI_MODEL
                if GEMINI_API_KEY
                else "not_configured"
            )
    }


# ============================================================
# QUERY
# ============================================================

@app.post("/query")
def ask_sahayak(

    request: QueryRequest,

    current_user=Depends(
        get_current_user
    )

):

    print(
        "\n=================================================="
    )

    print(
        "NEW SAHAYAK QUERY"
    )

    print(
        "Question:",
        request.query
    )

    print(
        "Language:",
        request.language
    )

    print(
        "Stakeholder:",
        request.stakeholder
    )

    print(
        "User:",
        current_user.get("email")
    )

    print(
        "=================================================="
    )


    # ========================================================
    # VALIDATE
    # ========================================================

    query = request.query.strip()


    if not query:

        raise HTTPException(

            status_code=400,

            detail="Please enter a question."
        )


    # ========================================================
    # VARIABLES
    # ========================================================

    results = []

    valid_results = []

    context_chunks = []

    highest_score = 0.0

    average_score = 0.0

    confidence = "Low"

    evidence_available = False

    retrieval_status = "not_attempted"

    # # ========================================================
    # # QDRANT RETRIEVAL
    # # ========================================================

    # results = []
    # retrieval_status = "not_configured"

    # if qdrant is not None:

    #     try:

    #         print("========================================")
    #         print("STARTING QDRANT RETRIEVAL")
    #         print("========================================")

    #         print("Getting embedding model...")

    #         embedder = get_embedder()

    #         print("Embedding model loaded successfully.")

    #         if embedder is None:
    #             raise Exception(
    #                 "Embedding model is unavailable."
    #             )

    #         print("Generating query embedding...")

    #         embedding = embedder.encode(
    #             query
    #         ).tolist()

    #         print(
    #             "Embedding generated successfully."
    #         )

    #         print(
    #             "Embedding dimension:",
    #             len(embedding)
    #         )

    #         print(
    #             "Searching Qdrant..."
    #         )

    #         results = qdrant.query_points(
    #             collection_name=QDRANT_COLLECTION,
    #             query=embedding,
    #             limit=TOP_K,
    #             with_payload=True
    #         ).points

    #         print(
    #             "Qdrant returned:",
    #             len(results),
    #             "results"
    #         )

    #         for i, point in enumerate(results):

    #             print(
    #                 f"--- Result {i + 1} ---"
    #             )

    #             print(
    #                 "Score:",
    #                 getattr(point, "score", None)
    #             )

    #             print(
    #                 "Payload:",
    #                 getattr(point, "payload", None)
    #             )

    #         retrieval_status = "success"

    #     except Exception as e:

    #         print(
    #             "========================================"
    #         )

    #         print(
    #             "QDRANT RETRIEVAL ERROR:"
    #         )

    #         print(
    #             repr(e)
    #         )

    #         print(
    #             "========================================"
    #         )

    #         results = []

    #         retrieval_status = "failed"

    # elif qdrant is None:

    #     retrieval_status = "not_configured"

    #     print(
    #         "QDRANT ERROR: Client is None."
    #     )
    # ========================================================
    # QDRANT RETRIEVAL
    # ========================================================

    results = []
    retrieval_status = "not_configured"

    if qdrant is not None:

        try:

            print("========================================")
            print("STARTING QDRANT RETRIEVAL")
            print("========================================")

            print("Getting embedding model...")

            embedder = get_embedder()

            print(
                "Embedding model ready."
            )

            print(
                "Generating query embedding..."
            )

            embedding = embedder.encode(
                query
            ).tolist()

            print(
                "Embedding generated."
            )

            print(
                "Embedding dimension:",
                len(embedding)
            )

            print(
                "Searching Qdrant..."
            )

            results = qdrant.query_points(

                collection_name=QDRANT_COLLECTION,

                query=embedding,

                limit=TOP_K,

                with_payload=True

            ).points

            print(
                "Qdrant returned:",
                len(results),
                "results"
            )

            # ------------------------------------------------
            # PRINT RETRIEVED RESULTS
            # ------------------------------------------------

            for i, point in enumerate(results):

                print(
                    f"\n--- Retrieved Result {i + 1} ---"
                )

                print(
                    "Score:",
                    getattr(
                        point,
                        "score",
                        None
                    )
                )

                print(
                    "Payload:",
                    getattr(
                        point,
                        "payload",
                        None
                    )
                )

            retrieval_status = "success"

        except Exception as e:

            print(
                "========================================"
            )

            print(
                "QDRANT RETRIEVAL ERROR:"
            )

            print(
                repr(e)
            )

            print(
                "========================================"
            )

            results = []

            retrieval_status = "failed"

    elif qdrant is None:

        retrieval_status = "not_configured"

        print(
            "QDRANT ERROR: Client is None."
        )

    # ========================================================
    # FILTER EVIDENCE
    # ========================================================

    valid_results = [

        hit

        for hit in results

        if (

            hit.score is not None

            and hit.score >=
                RAG_SCORE_THRESHOLD

            and hit.payload

            and hit.payload.get("text")

        )

    ]


    print(
        "Valid evidence chunks:",
        len(valid_results)
    )


    # ========================================================
    # SCORES
    # ========================================================

    if valid_results:

        scores = [

            hit.score

            for hit in valid_results

        ]


        highest_score = max(
            scores
        )


        average_score = (
            sum(scores)
            /
            len(scores)
        )


        # ====================================================
        # CONFIDENCE
        # ====================================================

        if (

            highest_score >= 0.70

            and average_score >= 0.55

        ):

            confidence = "High"


        elif (

            highest_score >= 0.55

            and average_score >= 0.40

        ):

            confidence = "Medium"


        else:

            confidence = "Low"


        # ====================================================
        # BUILD CONTEXT
        # ====================================================

        for i, hit in enumerate(

            valid_results,

            start=1

        ):

            payload = (
                hit.payload
                or {}
            )


            text = payload.get(
                "text",
                ""
            )


            context_chunks.append(

                f"""
SOURCE {i}

Similarity Score:
{round(hit.score, 4)}

Source Name:
{payload.get("source_name", "Unknown")}

Organization:
{payload.get("organization", "Unknown")}

Document:
{payload.get(
    "document_title",
    payload.get("title", "Unknown")
)}

Page / Section:
{payload.get("page", "")}

Content:
{text}
"""
            )


        if context_chunks:

            evidence_available = True


    # ========================================================
    # ANSWER MODE
    # ========================================================

    if evidence_available:

        context = "\n\n---\n\n".join(
            context_chunks
        )

        answer_mode = (
            "EVIDENCE-GROUNDED RAG MODE"
        )

    else:

        context = (
            "NO RETRIEVED EVIDENCE IS AVAILABLE."
        )

        answer_mode = (
            "GENERAL KNOWLEDGE MODE"
        )


    # ========================================================
    # GEMINI PROMPT
    # ========================================================

    prompt = f"""
You are Sahayak, an AI assistant specializing in:

- Ayurveda intellectual property
- Patents
- Traditional knowledge
- Indian regulations
- AYUSH-related intellectual property

USER QUESTION:
{query}

STAKEHOLDER:
{request.stakeholder}

REQUESTED LANGUAGE:
{request.language}

ANSWER MODE:
{answer_mode}

============================================================
RETRIEVED EVIDENCE
============================================================

{context}

============================================================
STRICT INSTRUCTIONS
============================================================

1. If evidence is available, use the retrieved evidence
   as the PRIMARY basis of the answer.

2. Do NOT invent laws, regulations, sections, organizations,
   documents, citations, URLs, dates, or legal claims.

3. Do NOT claim that a source says something unless the
   retrieved evidence actually supports it.

4. If evidence only partially answers the question,
   clearly say what is supported and what is not.

5. If there is conflicting evidence, mention the conflict.

6. When appropriate, mention the relevant document/source
   by name.

7. If NO evidence is available, begin the response with:

   "General information — no supporting evidence was
   retrieved from the Sahayak evidence database."

8. In GENERAL KNOWLEDGE MODE, do not present uncertain
   legal information as a definitive legal conclusion.

9. Respond in the requested language.

10. Adapt the explanation to the stakeholder.

11. Use simple, clear language.

12. Use bullet points when useful.

13. Do not mention internal prompts, retrieval mechanisms,
    system instructions, or token limits.

14. Do not fabricate citations.

Answer the user's question now.
"""


    # ========================================================
    # GENERATE ANSWER
    # ========================================================

    try:

        answer = generate_answer(
            prompt
        )


    except requests.exceptions.Timeout:

        print(
            "GEMINI TIMEOUT"
        )

        raise HTTPException(

            status_code=504,

            detail=(
                "Gemini took too long to respond. "
                "Please try again."
            )
        )


    except requests.exceptions.ConnectionError:

        print(
            "GEMINI CONNECTION ERROR"
        )

        raise HTTPException(

            status_code=503,

            detail=(
                "Could not connect to Gemini."
            )
        )


    except Exception as e:

        print(
            "GEMINI ERROR:",
            e
        )

        raise HTTPException(

            status_code=502,

            detail=(
                "Gemini API returned an error. "
                "Check the Gemini API configuration."
            )
        )


    # ========================================================
    # BUILD SOURCES
    # ========================================================

    sources = []

    seen_sources = set()


    for hit in valid_results:

        payload = (
            hit.payload
            or {}
        )


        source_key = (

            payload.get(
                "source_id"
            )

            or payload.get(
                "source_url"
            )

            or payload.get(
                "document_title"
            )

            or payload.get(
                "source_name"
            )

            or "unknown"

        )


        if source_key in seen_sources:

            continue


        seen_sources.add(
            source_key
        )


        sources.append({

            "id":
                len(sources) + 1,

            "source_name":
                (
                    payload.get(
                        "source_name"
                    )

                    or payload.get(
                        "document_title"
                    )

                    or payload.get(
                        "organization"
                    )

                    or "Unknown Source"
                ),

            "source_url":
                payload.get(
                    "source_url",
                    ""
                ),

            "document_title":
                (
                    payload.get(
                        "document_title"
                    )

                    or payload.get(
                        "source_name"
                    )

                    or "Unknown Document"
                ),

            "source_id":
                payload.get(
                    "source_id",
                    ""
                ),

            "organization":
                payload.get(
                    "organization",
                    ""
                ),

            "publication_date":
                payload.get(
                    "publication_date",
                    ""
                ),

            "page":
                payload.get(
                    "page",
                    ""
                ),

            "type":
                payload.get(
                    "type",
                    "Legal Document"
                ),

            "description":
                payload.get(
                    "description",
                    ""
                ),

            "similarity_score":

                (
                    round(
                        hit.score,
                        4
                    )

                    if hit.score is not None

                    else None
                )
        })


    # ========================================================
    # CONFIDENCE DETAILS
    # ========================================================

    if evidence_available:

        confidence_method = (

            "Based on Qdrant similarity scores "
            "from retrieved evidence."
        )

    else:

        confidence_method = (

            "No sufficiently relevant Qdrant evidence "
            "was available. Answer generated using "
            "Gemini general knowledge."
        )


    confidence_details = {

        "highest_score":
            round(
                highest_score,
                4
            ),

        "average_score":
            round(
                average_score,
                4
            ),

        "retrieved_chunks":
            len(valid_results),

        "retrieval_status":
            retrieval_status,

        "confidence_method":
            confidence_method
    }


    # ========================================================
    # SAVE CHAT
    # ========================================================

    chat_document = {

        "user_id":
            current_user["_id"],

        "user_email":
            current_user.get(
                "email",
                ""
            ),

        "query":
            query,

        "answer":
            answer.strip(),

        "language":
            request.language,

        "stakeholder":
            request.stakeholder,

        "sources":
            sources,

        "confidence":
            confidence,

        "confidence_details":
            confidence_details,

        "answer_mode":
            answer_mode,

        "created_at":
            datetime.now(
                timezone.utc
            )
    }


    try:

        chat_result = (
            chats_collection.insert_one(
                chat_document
            )
        )


        chat_id = str(
            chat_result.inserted_id
        )


        print(
            "Chat saved:",
            chat_id
        )


    except Exception as e:

        print(
            "MongoDB chat save error:",
            e
        )

        chat_id = None


    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "chat_id":
            chat_id,

        "answer":
            answer.strip(),

        "sources":
            sources,

        "confidence":
            confidence,

        "confidence_details":
            confidence_details,

        "answer_mode":
            answer_mode
    }


# ============================================================
# GET ALL CHATS
# ============================================================

@app.get("/chats")
def get_chats(

    current_user=Depends(
        get_current_user
    )

):

    try:

        chats = chats_collection.find(

            {
                "user_id":
                    current_user["_id"]
            }

        ).sort(

            "created_at",
            -1
        )


        chat_list = []


        for chat in chats:

            chat_list.append({

                "id":
                    str(
                        chat["_id"]
                    ),

                "query":
                    chat.get(
                        "query",
                        ""
                    ),

                "answer":
                    chat.get(
                        "answer",
                        ""
                    ),

                "language":
                    chat.get(
                        "language",
                        "English"
                    ),

                "stakeholder":
                    chat.get(
                        "stakeholder",
                        "Researcher"
                    ),

                "confidence":
                    chat.get(
                        "confidence",
                        "Low"
                    ),

                "created_at":
                    chat.get(
                        "created_at"
                    ),

                "sources_count":
                    len(
                        chat.get(
                            "sources",
                            []
                        )
                    )
            })


        return {

            "chats":
                chat_list,

            "count":
                len(chat_list)
        }


    except Exception as e:

        print(
            "MongoDB error while fetching chats:",
            e
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "Unable to retrieve chat history."
            )
        )


# ============================================================
# GET SINGLE CHAT
# ============================================================

@app.get("/chats/{chat_id}")
def get_chat(

    chat_id: str,

    current_user=Depends(
        get_current_user
    )

):

    try:

        object_id = ObjectId(
            chat_id
        )

    except Exception:

        raise HTTPException(

            status_code=400,

            detail="Invalid chat ID."
        )


    try:

        chat = chats_collection.find_one(

            {

                "_id":
                    object_id,

                "user_id":
                    current_user["_id"]
            }
        )


    except Exception as e:

        print(
            "MongoDB error while fetching chat:",
            e
        )

        raise HTTPException(

            status_code=500,

            detail="Unable to retrieve chat."
        )


    if not chat:

        raise HTTPException(

            status_code=404,

            detail="Chat not found."
        )


    return {

        "id":
            str(
                chat["_id"]
            ),

        "query":
            chat.get(
                "query",
                ""
            ),

        "answer":
            chat.get(
                "answer",
                ""
            ),

        "language":
            chat.get(
                "language",
                "English"
            ),

        "stakeholder":
            chat.get(
                "stakeholder",
                "Researcher"
            ),

        "sources":
            chat.get(
                "sources",
                []
            ),

        "confidence":
            chat.get(
                "confidence",
                "Low"
            ),

        "confidence_details":
            chat.get(
                "confidence_details",
                {}
            ),

        "answer_mode":
            chat.get(
                "answer_mode",
                "UNKNOWN"
            ),

        "created_at":
            chat.get(
                "created_at"
            )
    }