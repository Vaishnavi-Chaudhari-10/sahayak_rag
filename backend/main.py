

# # # import os

# # # import requests

# # # from datetime import (
# # #     datetime,
# # #     timezone
# # # )

# # # from bson import ObjectId

# # # from dotenv import load_dotenv

# # # from fastapi import (
# # #     FastAPI,
# # #     Depends,
# # #     HTTPException,
# # #     status
# # # )

# # # from fastapi.middleware.cors import (
# # #     CORSMiddleware
# # # )

# # # from pydantic import BaseModel

# # # from qdrant_client import QdrantClient

# # # from sentence_transformers import (
# # #     SentenceTransformer
# # # )

# # # from auth import (
# # #     router as auth_router,
# # #     get_current_user
# # # )

# # # from database import (
# # #     chats_collection
# # # )


# # # # ============================================================
# # # # LOAD ENVIRONMENT VARIABLES
# # # # ============================================================

# # # load_dotenv()


# # # # ============================================================
# # # # FRONTEND
# # # # ============================================================

# # # FRONTEND_URL = os.getenv(
# # #     "FRONTEND_URL",
# # #     "http://localhost:5173"
# # # )


# # # # ============================================================
# # # # QDRANT
# # # # ============================================================

# # # QDRANT_URL = os.getenv(
# # #     "QDRANT_URL",
# # #     ""
# # # )

# # # QDRANT_API_KEY = os.getenv(
# # #     "QDRANT_API_KEY",
# # #     ""
# # # )

# # # QDRANT_COLLECTION = os.getenv(
# # #     "QDRANT_COLLECTION",
# # #     "ayurveda_ip"
# # # )


# # # # ============================================================
# # # # OLLAMA
# # # # ============================================================

# # # OLLAMA_URL = os.getenv(
# # #     "OLLAMA_URL",
# # #     "http://localhost:11434/api/generate"
# # # )

# # # OLLAMA_MODEL = os.getenv(
# # #     "OLLAMA_MODEL",
# # #     "qwen2.5:7b"
# # # )


# # # # ============================================================
# # # # OPTIONAL CLOUD LLM
# # # # ============================================================

# # # LLM_API_URL = os.getenv(
# # #     "LLM_API_URL",
# # #     ""
# # # )

# # # LLM_API_KEY = os.getenv(
# # #     "LLM_API_KEY",
# # #     ""
# # # )

# # # LLM_MODEL = os.getenv(
# # #     "LLM_MODEL",
# # #     ""
# # # )


# # # # ============================================================
# # # # FASTAPI
# # # # ============================================================

# # # app = FastAPI(

# # #     title="Sahayak API",

# # #     description=(
# # #         "AI Assistant for "
# # #         "Ayurveda IP & Regulation"
# # #     ),

# # #     version="1.0.0"
# # # )


# # # # ============================================================
# # # # CORS
# # # # ============================================================

# # # allowed_origins = [

# # #     FRONTEND_URL,

# # #     "http://localhost:5173",

# # #     "http://127.0.0.1:5173"
# # # ]


# # # allowed_origins = list(
# # #     dict.fromkeys(

# # #         origin.rstrip("/")

# # #         for origin in allowed_origins

# # #         if origin
# # #     )
# # # )


# # # app.add_middleware(

# # #     CORSMiddleware,

# # #     allow_origins=allowed_origins,

# # #     allow_credentials=True,

# # #     allow_methods=["*"],

# # #     allow_headers=["*"]
# # # )


# # # # ============================================================
# # # # AUTH ROUTER
# # # # ============================================================

# # # app.include_router(
# # #     auth_router
# # # )


# # # # ============================================================
# # # # REQUEST MODEL
# # # # ============================================================

# # # class QueryRequest(BaseModel):

# # #     query: str

# # #     language: str = "English"

# # #     stakeholder: str = "Researcher"


# # # # ============================================================
# # # # QDRANT INITIALIZATION
# # # # ============================================================

# # # qdrant = None


# # # if QDRANT_URL and QDRANT_API_KEY:

# # #     try:

# # #         qdrant = QdrantClient(

# # #             url=QDRANT_URL,

# # #             api_key=QDRANT_API_KEY
# # #         )


# # #         print(
# # #             "=================================================="
# # #         )

# # #         print(
# # #             "QDRANT: Connected to Qdrant Cloud"
# # #         )

# # #         print(
# # #             "Collection:",
# # #             QDRANT_COLLECTION
# # #         )

# # #         print(
# # #             "=================================================="
# # #         )

# # #     except Exception as e:

# # #         print(
# # #             "QDRANT INITIALIZATION ERROR:",
# # #             e
# # #         )

# # #         qdrant = None

# # # else:

# # #     print(
# # #         "=================================================="
# # #     )

# # #     print(
# # #         "QDRANT: Not configured"
# # #     )

# # #     print(
# # #         "Sahayak can use general knowledge "
# # #         "when evidence is unavailable."
# # #     )

# # #     print(
# # #         "=================================================="
# # #     )


# # # # ============================================================
# # # # EMBEDDING MODEL
# # # # ============================================================

# # # embedder = None


# # # try:

# # #     print(
# # #         "Loading embedding model..."
# # #     )


# # #     embedder = SentenceTransformer(
# # #         "all-MiniLM-L6-v2"
# # #     )


# # #     print(
# # #         "Embedding model loaded successfully."
# # #     )

# # # except Exception as e:

# # #     print(
# # #         "Embedding model initialization error:",
# # #         e
# # #     )

# # #     embedder = None


# # # # ============================================================
# # # # LLM GENERATION
# # # # ============================================================

# # # def generate_answer(
# # #     prompt: str
# # # ) -> str:

# # #     # ========================================================
# # #     # CLOUD LLM
# # #     # ========================================================

# # #     if (
# # #         LLM_API_URL
# # #         and LLM_API_KEY
# # #         and LLM_MODEL
# # #     ):

# # #         print(
# # #             "Using cloud LLM:",
# # #             LLM_MODEL
# # #         )


# # #         headers = {

# # #             "Authorization":
# # #                 f"Bearer {LLM_API_KEY}",

# # #             "Content-Type":
# # #                 "application/json"
# # #         }


# # #         payload = {

# # #             "model":
# # #                 LLM_MODEL,

# # #             "messages": [

# # #                 {

# # #                     "role":
# # #                         "user",

# # #                     "content":
# # #                         prompt
# # #                 }

# # #             ],

# # #             "temperature":
# # #                 0.2
# # #         }


# # #         response = requests.post(

# # #             LLM_API_URL,

# # #             headers=headers,

# # #             json=payload,

# # #             timeout=120
# # #         )


# # #         response.raise_for_status()


# # #         data = response.json()


# # #         try:

# # #             answer = data[
# # #                 "choices"
# # #             ][
# # #                 0
# # #             ][
# # #                 "message"
# # #             ][
# # #                 "content"
# # #             ]


# # #             return answer.strip()

# # #         except (
# # #             KeyError,
# # #             IndexError,
# # #             TypeError
# # #         ):

# # #             raise RuntimeError(
# # #                 "Unexpected cloud LLM response format."
# # #             )


# # #     # ========================================================
# # #     # OLLAMA
# # #     # ========================================================

# # #     if OLLAMA_URL:

# # #         print(
# # #             "Using Ollama:",
# # #             OLLAMA_MODEL
# # #         )


# # #         payload = {

# # #             "model":
# # #                 OLLAMA_MODEL,

# # #             "prompt":
# # #                 prompt,

# # #             "stream":
# # #                 False,

# # #             "options": {

# # #                 "temperature":
# # #                     0.2
# # #             }
# # #         }


# # #         response = requests.post(

# # #             OLLAMA_URL,

# # #             json=payload,

# # #             timeout=180
# # #         )


# # #         response.raise_for_status()


# # #         data = response.json()


# # #         answer = data.get(
# # #             "response",
# # #             ""
# # #         )


# # #         if not answer:

# # #             raise RuntimeError(
# # #                 "Ollama returned an empty response."
# # #             )


# # #         return answer.strip()


# # #     # ========================================================
# # #     # NO LLM
# # #     # ========================================================

# # #     raise RuntimeError(

# # #         "No LLM is configured. "
# # #         "Configure Ollama or a cloud LLM."
# # #     )


# # # # ============================================================
# # # # HOME
# # # # ============================================================

# # # @app.get("/")
# # # def home():

# # #     return {

# # #         "message":
# # #             "Sahayak backend is running",

# # #         "status":
# # #             "online",

# # #         "service":
# # #             "Sahayak API",

# # #         "version":
# # #             "1.0.0"
# # #     }


# # # # ============================================================
# # # # HEALTH
# # # # ============================================================

# # # @app.get("/health")
# # # def health():

# # #     return {

# # #         "status":
# # #             "healthy",

# # #         "qdrant":
# # #             (
# # #                 "connected"
# # #                 if qdrant is not None
# # #                 else "not_configured"
# # #             ),

# # #         "embedding_model":
# # #             (
# # #                 "loaded"
# # #                 if embedder is not None
# # #                 else "unavailable"
# # #             ),

# # #         "ollama":
# # #             (
# # #                 OLLAMA_MODEL
# # #                 if OLLAMA_URL
# # #                 else "not_configured"
# # #             ),

# # #         "cloud_llm":
# # #             (
# # #                 LLM_MODEL

# # #                 if (
# # #                     LLM_API_URL
# # #                     and LLM_API_KEY
# # #                     and LLM_MODEL
# # #                 )

# # #                 else "not_configured"
# # #             )
# # #     }


# # # # ============================================================
# # # # QUERY
# # # # ============================================================

# # # @app.post("/query")
# # # def ask_sahayak(

# # #     request: QueryRequest,

# # #     current_user=Depends(
# # #         get_current_user
# # #     )
# # # ):

# # #     print(
# # #         "\n=================================================="
# # #     )

# # #     print(
# # #         "NEW SAHAYAK QUERY"
# # #     )

# # #     print(
# # #         "=================================================="
# # #     )

# # #     print(
# # #         "Question:",
# # #         request.query
# # #     )

# # #     print(
# # #         "Language:",
# # #         request.language
# # #     )

# # #     print(
# # #         "Stakeholder:",
# # #         request.stakeholder
# # #     )

# # #     print(
# # #         "User:",
# # #         current_user.get("email")
# # #     )


# # #     # ========================================================
# # #     # VALIDATE QUERY
# # #     # ========================================================

# # #     query = request.query.strip()


# # #     if not query:

# # #         return {

# # #             "answer":
# # #                 "Please enter a question.",

# # #             "sources":
# # #                 [],

# # #             "confidence":
# # #                 "Low",

# # #             "confidence_details": {

# # #                 "highest_score":
# # #                     0,

# # #                 "average_score":
# # #                     0,

# # #                 "retrieved_chunks":
# # #                     0,

# # #                 "retrieval_status":
# # #                     "not_attempted",

# # #                 "confidence_method":
# # #                     "No question was provided."
# # #             },

# # #             "answer_mode":
# # #                 "NO_QUERY"
# # #         }


# # #     # ========================================================
# # #     # VARIABLES
# # #     # ========================================================

# # #     results = []

# # #     context_chunks = []

# # #     highest_score = 0

# # #     average_score = 0

# # #     confidence = "Low"

# # #     evidence_available = False

# # #     retrieval_status = "not_attempted"


# # #     # ========================================================
# # #     # QDRANT RETRIEVAL
# # #     # ========================================================

# # #     if (
# # #         qdrant is not None
# # #         and embedder is not None
# # #     ):

# # #         try:

# # #             print(
# # #                 "Generating query embedding..."
# # #             )


# # #             embedding = embedder.encode(
# # #                 query
# # #             ).tolist()


# # #             print(
# # #                 "Searching Qdrant..."
# # #             )


# # #             results = qdrant.query_points(

# # #                 collection_name=
# # #                     QDRANT_COLLECTION,

# # #                 query=
# # #                     embedding,

# # #                 limit=5

# # #             ).points


# # #             retrieval_status = "success"


# # #             print(
# # #                 "Retrieved chunks:",
# # #                 len(results)
# # #             )


# # #         except Exception as e:

# # #             print(
# # #                 "QDRANT RETRIEVAL ERROR:",
# # #                 e
# # #             )

# # #             results = []

# # #             retrieval_status = "failed"


# # #     elif qdrant is None:

# # #         retrieval_status = "not_configured"


# # #     elif embedder is None:

# # #         retrieval_status = "embedding_unavailable"


# # #     # ========================================================
# # #     # PROCESS RESULTS
# # #     # ========================================================

# # #     if results:

# # #         scores = [

# # #             hit.score

# # #             for hit in results

# # #             if hit.score is not None
# # #         ]


# # #         if scores:

# # #             highest_score = max(
# # #                 scores
# # #             )

# # #             average_score = (
# # #                 sum(scores)
# # #                 /
# # #                 len(scores)
# # #             )


# # #         print(
# # #             "QDRANT SCORES:",
# # #             [
# # #                 round(
# # #                     score,
# # #                     4
# # #                 )
# # #                 for score in scores
# # #             ]
# # #         )


# # #         # ----------------------------------------------------
# # #         # CONFIDENCE
# # #         # ----------------------------------------------------

# # #         if (

# # #             highest_score >= 0.70

# # #             and average_score >= 0.55

# # #         ):

# # #             confidence = "High"


# # #         elif (

# # #             highest_score >= 0.55

# # #             and average_score >= 0.40

# # #         ):

# # #             confidence = "Medium"


# # #         else:

# # #             confidence = "Low"


# # #         # ----------------------------------------------------
# # #         # BUILD CONTEXT
# # #         # ----------------------------------------------------

# # #         for i, hit in enumerate(

# # #             results,

# # #             start=1
# # #         ):

# # #             payload = (
# # #                 hit.payload
# # #                 or {}
# # #             )


# # #             text = payload.get(
# # #                 "text",
# # #                 ""
# # #             )


# # #             if not text:

# # #                 continue


# # #             context_chunks.append(

# # #                 f"""
# # # SOURCE {i}

# # # Similarity Score:
# # # {
# # #     round(hit.score, 4)
# # #     if hit.score is not None
# # #     else "N/A"
# # # }

# # # Source Name:
# # # {
# # #     payload.get(
# # #         "source_name",
# # #         "Unknown"
# # #     )
# # # }

# # # Organization:
# # # {
# # #     payload.get(
# # #         "organization",
# # #         "Unknown"
# # #     )
# # # }

# # # Document:
# # # {
# # #     payload.get(
# # #         "document_title",
# # #         payload.get(
# # #             "title",
# # #             "Unknown"
# # #         )
# # #     )
# # # }

# # # Page / Section:
# # # {
# # #     payload.get(
# # #         "page",
# # #         ""
# # #     )
# # # }

# # # Content:
# # # {text}
# # # """
# # #             )


# # #         if context_chunks:

# # #             evidence_available = True


# # #     # ========================================================
# # #     # BUILD CONTEXT
# # #     # ========================================================

# # #     if evidence_available:

# # #         context = "\n\n---\n\n".join(
# # #             context_chunks
# # #         )

# # #         answer_mode = (
# # #             "EVIDENCE-GROUNDED RAG MODE"
# # #         )

# # #     else:

# # #         context = (
# # #             "NO RETRIEVED EVIDENCE IS AVAILABLE."
# # #         )

# # #         answer_mode = (
# # #             "GENERAL KNOWLEDGE MODE"
# # #         )


# # #     # ========================================================
# # #     # PROMPT
# # #     # ========================================================

# # #     prompt = f"""
# # # You are Sahayak, an AI assistant specializing in
# # # Ayurveda intellectual property, patents, traditional
# # # knowledge, and Indian regulations.

# # # ============================================================
# # # USER QUESTION
# # # ============================================================

# # # {query}

# # # ============================================================
# # # STAKEHOLDER
# # # ============================================================

# # # {request.stakeholder}

# # # ============================================================
# # # REQUESTED LANGUAGE
# # # ============================================================

# # # {request.language}

# # # ============================================================
# # # ANSWER MODE
# # # ============================================================

# # # {answer_mode}

# # # ============================================================
# # # RETRIEVED EVIDENCE
# # # ============================================================

# # # {context}

# # # ============================================================
# # # IMPORTANT INSTRUCTIONS
# # # ============================================================

# # # MODE 1 — EVIDENCE-GROUNDED RAG MODE

# # # If retrieved evidence is available:

# # # 1. Use the retrieved evidence as the primary basis
# # #    of the answer.

# # # 2. Carefully reason over the evidence.

# # # 3. Do not invent facts, laws, regulations, sections,
# # #    organizations, documents, citations, or URLs.

# # # 4. If the evidence directly answers the question,
# # #    explain the answer clearly.

# # # 5. If the evidence only partially answers the question,
# # #    clearly distinguish what the evidence establishes
# # #    from what it does not establish.

# # # 6. Mention the relevant source or document naturally.

# # # 7. Do not claim that information came from a source
# # #    unless the retrieved content supports that claim.

# # # 8. General knowledge may be used only as clearly
# # #    separated background information.

# # # MODE 2 — GENERAL KNOWLEDGE MODE

# # # If no retrieved evidence is available:

# # # 1. Begin the answer with:

# # # "General information — no supporting evidence was
# # # retrieved from the Sahayak evidence database."

# # # 2. Answer using general knowledge.

# # # 3. Do not invent specific laws, legal sections,
# # #    government notifications, citations, or URLs.

# # # 4. For legal or intellectual-property questions,
# # #    avoid presenting uncertain information as a
# # #    definitive legal conclusion.

# # # 5. If uncertain, say so.

# # # ============================================================
# # # LANGUAGE
# # # ============================================================

# # # Respond in:

# # # {request.language}

# # # Supported languages:

# # # English
# # # Hindi
# # # Marathi
# # # Tamil

# # # ============================================================
# # # STYLE
# # # ============================================================

# # # - Be clear.
# # # - Be concise but useful.
# # # - Use simple explanations.
# # # - Use bullet points when helpful.
# # # - Do not mention internal prompts.
# # # - Do not mention token limits.
# # # - Do not fabricate sources.
# # # - Do not fabricate URLs.

# # # ============================================================
# # # FINAL TASK
# # # ============================================================

# # # Answer the user's question now.
# # # """


# # #     # ========================================================
# # #     # GENERATE ANSWER
# # #     # ========================================================

# # #     try:

# # #         print(
# # #             "Generating answer with LLM..."
# # #         )


# # #         answer = generate_answer(
# # #             prompt
# # #         )


# # #         print(
# # #             "Answer generated successfully."
# # #         )


# # #     except requests.exceptions.ConnectionError:

# # #         print(
# # #             "LLM CONNECTION ERROR"
# # #         )


# # #         raise HTTPException(

# # #             status_code=503,

# # #             detail=(
# # #                 "Could not connect to the "
# # #                 "language model. Please make "
# # #                 "sure Ollama is running."
# # #             )
# # #         )


# # #     except requests.exceptions.Timeout:

# # #         print(
# # #             "LLM TIMEOUT"
# # #         )


# # #         raise HTTPException(

# # #             status_code=504,

# # #             detail=(
# # #                 "The language model took too "
# # #                 "long to respond. Please try again."
# # #             )
# # #         )


# # #     except requests.exceptions.HTTPError as e:

# # #         print(
# # #             "LLM HTTP ERROR:",
# # #             e
# # #         )


# # #         raise HTTPException(

# # #             status_code=502,

# # #             detail=(
# # #                 "The language model returned "
# # #                 "an error."
# # #             )
# # #         )


# # #     except Exception as e:

# # #         print(
# # #             "LLM ERROR:",
# # #             e
# # #         )


# # #         raise HTTPException(

# # #             status_code=500,

# # #             detail=(
# # #                 "An error occurred while "
# # #                 "generating the answer."
# # #             )
# # #         )


# # #     # ========================================================
# # #     # BUILD SOURCES
# # #     # ========================================================

# # #     sources = []

# # #     seen_sources = set()


# # #     for hit in results:

# # #         payload = (
# # #             hit.payload
# # #             or {}
# # #         )


# # #         source_key = (

# # #             payload.get(
# # #                 "source_id"
# # #             )

# # #             or payload.get(
# # #                 "source_url"
# # #             )

# # #             or payload.get(
# # #                 "document_title"
# # #             )

# # #             or payload.get(
# # #                 "source_name"
# # #             )

# # #             or "unknown"
# # #         )


# # #         if source_key in seen_sources:

# # #             continue


# # #         seen_sources.add(
# # #             source_key
# # #         )


# # #         sources.append({

# # #             "id":
# # #                 len(sources) + 1,

# # #             "source_name":
# # #                 (
# # #                     payload.get(
# # #                         "source_name"
# # #                     )

# # #                     or payload.get(
# # #                         "document_title"
# # #                     )

# # #                     or payload.get(
# # #                         "organization"
# # #                     )

# # #                     or "Unknown Source"
# # #                 ),

# # #             "source_url":
# # #                 payload.get(
# # #                     "source_url",
# # #                     ""
# # #                 ),

# # #             "document_title":
# # #                 (
# # #                     payload.get(
# # #                         "document_title"
# # #                     )

# # #                     or payload.get(
# # #                         "source_name"
# # #                     )

# # #                     or "Unknown Document"
# # #                 ),

# # #             "source_id":
# # #                 payload.get(
# # #                     "source_id",
# # #                     ""
# # #                 ),

# # #             "organization":
# # #                 payload.get(
# # #                     "organization",
# # #                     ""
# # #                 ),

# # #             "publication_date":
# # #                 payload.get(
# # #                     "publication_date",
# # #                     ""
# # #                 ),

# # #             "page":
# # #                 payload.get(
# # #                     "page",
# # #                     ""
# # #                 ),

# # #             "type":
# # #                 payload.get(
# # #                     "type",
# # #                     "Legal Document"
# # #                 ),

# # #             "description":
# # #                 payload.get(
# # #                     "description",
# # #                     ""
# # #                 ),

# # #             "similarity_score":

# # #                 (
# # #                     round(
# # #                         hit.score,
# # #                         4
# # #                     )

# # #                     if hit.score is not None

# # #                     else None
# # #                 )
# # #         })


# # #     # ========================================================
# # #     # CONFIDENCE DETAILS
# # #     # ========================================================

# # #     if evidence_available:

# # #         confidence_method = (

# # #             "Based on Qdrant similarity scores "
# # #             "using highest and average evidence "
# # #             "relevance."
# # #         )

# # #     else:

# # #         confidence_method = (

# # #             "No Qdrant evidence was available. "
# # #             "Answer generated using general "
# # #             "LLM knowledge."
# # #         )


# # #     confidence_details = {

# # #         "highest_score":
# # #             round(
# # #                 highest_score,
# # #                 4
# # #             ),

# # #         "average_score":
# # #             round(
# # #                 average_score,
# # #                 4
# # #             ),

# # #         "retrieved_chunks":
# # #             len(results),

# # #         "retrieval_status":
# # #             retrieval_status,

# # #         "confidence_method":
# # #             confidence_method
# # #     }


# # #     # ========================================================
# # #     # SAVE CHAT
# # #     # ========================================================

# # #     chat_document = {

# # #         "user_id":
# # #             current_user["_id"],

# # #         "user_email":
# # #             current_user.get(
# # #                 "email",
# # #                 ""
# # #             ),

# # #         "query":
# # #             query,

# # #         "answer":
# # #             answer.strip(),

# # #         "language":
# # #             request.language,

# # #         "stakeholder":
# # #             request.stakeholder,

# # #         "sources":
# # #             sources,

# # #         "confidence":
# # #             confidence,

# # #         "confidence_details":
# # #             confidence_details,

# # #         "answer_mode":
# # #             answer_mode,

# # #         "created_at":
# # #             datetime.now(
# # #                 timezone.utc
# # #             )
# # #     }


# # #     chat_id = None


# # #     try:

# # #         chat_result = (
# # #             chats_collection.insert_one(
# # #                 chat_document
# # #             )
# # #         )


# # #         chat_id = str(
# # #             chat_result.inserted_id
# # #         )


# # #         print(
# # #             "Chat saved:",
# # #             chat_id
# # #         )


# # #     except Exception as e:

# # #         print(
# # #             "MongoDB chat save error:",
# # #             e
# # #         )


# # #     # ========================================================
# # #     # RESPONSE
# # #     # ========================================================

# # #     return {

# # #         "chat_id":
# # #             chat_id,

# # #         "answer":
# # #             answer.strip(),

# # #         "sources":
# # #             sources,

# # #         "confidence":
# # #             confidence,

# # #         "confidence_details":
# # #             confidence_details,

# # #         "answer_mode":
# # #             answer_mode
# # #     }


# # # # ============================================================
# # # # GET ALL CHATS
# # # # ============================================================

# # # @app.get("/chats")
# # # def get_chats(

# # #     current_user=Depends(
# # #         get_current_user
# # #     )

# # # ):

# # #     try:

# # #         chats = chats_collection.find(

# # #             {
# # #                 "user_id":
# # #                     current_user["_id"]
# # #             }

# # #         ).sort(

# # #             "created_at",
# # #             -1
# # #         )


# # #         chat_list = []


# # #         for chat in chats:

# # #             chat_list.append({

# # #                 "id":
# # #                     str(
# # #                         chat["_id"]
# # #                     ),

# # #                 "query":
# # #                     chat.get(
# # #                         "query",
# # #                         ""
# # #                     ),

# # #                 "answer":
# # #                     chat.get(
# # #                         "answer",
# # #                         ""
# # #                     ),

# # #                 "language":
# # #                     chat.get(
# # #                         "language",
# # #                         "English"
# # #                     ),

# # #                 "stakeholder":
# # #                     chat.get(
# # #                         "stakeholder",
# # #                         "Researcher"
# # #                     ),

# # #                 "confidence":
# # #                     chat.get(
# # #                         "confidence",
# # #                         "Low"
# # #                     ),

# # #                 "created_at":
# # #                     chat.get(
# # #                         "created_at"
# # #                     ),

# # #                 "sources_count":
# # #                     len(
# # #                         chat.get(
# # #                             "sources",
# # #                             []
# # #                         )
# # #                     )
# # #             })


# # #         return {

# # #             "chats":
# # #                 chat_list,

# # #             "count":
# # #                 len(chat_list)
# # #         }


# # #     except Exception as e:

# # #         print(
# # #             "MongoDB error while fetching chats:",
# # #             e
# # #         )


# # #         raise HTTPException(

# # #             status_code=500,

# # #             detail=(
# # #                 "Unable to retrieve chat history."
# # #             )
# # #         )


# # # # ============================================================
# # # # GET SINGLE CHAT
# # # # ============================================================

# # # @app.get("/chats/{chat_id}")
# # # def get_chat(

# # #     chat_id: str,

# # #     current_user=Depends(
# # #         get_current_user
# # #     )

# # # ):

# # #     # ========================================================
# # #     # VALIDATE OBJECT ID
# # #     # ========================================================

# # #     try:

# # #         object_id = ObjectId(
# # #             chat_id
# # #         )

# # #     except Exception:

# # #         raise HTTPException(

# # #             status_code=400,

# # #             detail="Invalid chat ID."
# # #         )


# # #     # ========================================================
# # #     # FIND CHAT
# # #     # ========================================================

# # #     try:

# # #         chat = chats_collection.find_one(

# # #             {

# # #                 "_id":
# # #                     object_id,

# # #                 "user_id":
# # #                     current_user["_id"]
# # #             }
# # #         )


# # #     except Exception as e:

# # #         print(
# # #             "MongoDB error while fetching chat:",
# # #             e
# # #         )


# # #         raise HTTPException(

# # #             status_code=500,

# # #             detail="Unable to retrieve chat."
# # #         )


# # #     # ========================================================
# # #     # CHAT NOT FOUND
# # #     # ========================================================

# # #     if not chat:

# # #         raise HTTPException(

# # #             status_code=404,

# # #             detail="Chat not found."
# # #         )


# # #     # ========================================================
# # #     # RESPONSE
# # #     # ========================================================

# # #     return {

# # #         "id":
# # #             str(
# # #                 chat["_id"]
# # #             ),

# # #         "query":
# # #             chat.get(
# # #                 "query",
# # #                 ""
# # #             ),

# # #         "answer":
# # #             chat.get(
# # #                 "answer",
# # #                 ""
# # #             ),

# # #         "language":
# # #             chat.get(
# # #                 "language",
# # #                 "English"
# # #             ),

# # #         "stakeholder":
# # #             chat.get(
# # #                 "stakeholder",
# # #                 "Researcher"
# # #             ),

# # #         "sources":
# # #             chat.get(
# # #                 "sources",
# # #                 []
# # #             ),

# # #         "confidence":
# # #             chat.get(
# # #                 "confidence",
# # #                 "Low"
# # #             ),

# # #         "confidence_details":
# # #             chat.get(
# # #                 "confidence_details",
# # #                 {}
# # #             ),

# # #         "answer_mode":
# # #             chat.get(
# # #                 "answer_mode",
# # #                 "UNKNOWN"
# # #             ),

# # #         "created_at":
# # #             chat.get(
# # #                 "created_at"
# # #             )
# # #     }
# # import os

# # from datetime import (
# #     datetime,
# #     timezone
# # )

# # import requests

# # from bson import ObjectId

# # from dotenv import load_dotenv

# # from fastapi import (
# #     FastAPI,
# #     Depends,
# #     HTTPException
# # )

# # from fastapi.middleware.cors import CORSMiddleware

# # from pydantic import BaseModel

# # from qdrant_client import QdrantClient

# # from sentence_transformers import SentenceTransformer

# # from auth import (
# #     router as auth_router,
# #     get_current_user
# # )

# # from database import chats_collection


# # # ============================================================
# # # LOAD ENVIRONMENT
# # # ============================================================

# # load_dotenv()


# # # ============================================================
# # # ENVIRONMENT SETTINGS
# # # ============================================================

# # FRONTEND_URL = os.getenv(
# #     "FRONTEND_URL",
# #     "http://localhost:5173"
# # )


# # # ============================================================
# # # QDRANT SETTINGS
# # # ============================================================
# # # ============================================================
# # # QDRANT SETTINGS
# # # ============================================================

# # QDRANT_URL = os.getenv(
# #     "CLOUD_QDRANT_URL",
# #     ""
# # )

# # QDRANT_API_KEY = os.getenv(
# #     "CLOUD_QDRANT_API_KEY",
# #     ""
# # )

# # QDRANT_COLLECTION = os.getenv(
# #     "QDRANT_COLLECTION",
# #     os.getenv(
# #         "COLLECTION_NAME",
# #         "ayurveda_ip"
# #     )
# # )
# # # QDRANT_URL = os.getenv(
# # #     "QDRANT_URL",
# # #     ""
# # # )

# # # QDRANT_API_KEY = os.getenv(
# # #     "QDRANT_API_KEY",
# # #     ""
# # # )

# # # QDRANT_COLLECTION = os.getenv(
# # #     "QDRANT_COLLECTION",
# # #     "ayurveda_ip"
# # # )


# # # ============================================================
# # # RAG SETTINGS
# # # ============================================================

# # # Only treat chunks above this score as useful evidence.

# # RAG_SCORE_THRESHOLD = float(
# #     os.getenv(
# #         "RAG_SCORE_THRESHOLD",
# #         "0.45"
# #     )
# # )


# # # ============================================================
# # # OLLAMA SETTINGS
# # # ============================================================

# # OLLAMA_URL = os.getenv(
# #     "OLLAMA_URL",
# #     "http://localhost:11434/api/generate"
# # )

# # OLLAMA_MODEL = os.getenv(
# #     "OLLAMA_MODEL",
# #     "qwen2.5:7b"
# # )


# # # ============================================================
# # # OPTIONAL CLOUD LLM
# # # ============================================================

# # LLM_API_URL = os.getenv(
# #     "LLM_API_URL",
# #     ""
# # )

# # LLM_API_KEY = os.getenv(
# #     "LLM_API_KEY",
# #     ""
# # )

# # LLM_MODEL = os.getenv(
# #     "LLM_MODEL",
# #     ""
# # )


# # # ============================================================
# # # FASTAPI
# # # ============================================================

# # app = FastAPI(
# #     title="Sahayak API",
# #     description=(
# #         "AI Assistant for Ayurveda IP & Regulation"
# #     ),
# #     version="1.0.0"
# # )


# # # ============================================================
# # # CORS
# # # ============================================================

# # allowed_origins = [

# #     FRONTEND_URL,

# #     "http://localhost:5173",

# #     "http://127.0.0.1:5173"
# # ]


# # allowed_origins = list(
# #     dict.fromkeys(
# #         origin.rstrip("/")
# #         for origin in allowed_origins
# #         if origin
# #     )
# # )


# # app.add_middleware(
# #     CORSMiddleware,

# #     allow_origins=allowed_origins,

# #     allow_credentials=True,

# #     allow_methods=["*"],

# #     allow_headers=["*"]
# # )


# # # ============================================================
# # # AUTH ROUTER
# # # ============================================================

# # app.include_router(
# #     auth_router
# # )


# # # ============================================================
# # # REQUEST MODEL
# # # ============================================================

# # class QueryRequest(BaseModel):

# #     query: str

# #     language: str = "English"

# #     stakeholder: str = "Researcher"


# # # ============================================================
# # # QDRANT
# # # ============================================================

# # qdrant = None


# # if QDRANT_URL and QDRANT_API_KEY:

# #     try:

# #         qdrant = QdrantClient(
# #             url=QDRANT_URL,
# #             api_key=QDRANT_API_KEY
# #         )

# #         print(
# #             "=================================================="
# #         )

# #         print(
# #             "QDRANT: Connected to Qdrant Cloud"
# #         )

# #         print(
# #             "Collection:",
# #             QDRANT_COLLECTION
# #         )

# #         print(
# #             "=================================================="
# #         )

# #     except Exception as e:

# #         print(
# #             "QDRANT INITIALIZATION ERROR:",
# #             e
# #         )

# #         qdrant = None

# # else:

# #     print(
# #         "=================================================="
# #     )

# #     print(
# #         "QDRANT: Not configured"
# #     )

# #     print(
# #         "Sahayak can still use Ollama."
# #     )

# #     print(
# #         "=================================================="
# #     )


# # # ============================================================
# # # EMBEDDING MODEL
# # # ============================================================

# # embedder = None


# # try:

# #     print(
# #         "Loading embedding model..."
# #     )

# #     embedder = SentenceTransformer(
# #         "all-MiniLM-L6-v2"
# #     )

# #     print(
# #         "Embedding model loaded successfully."
# #     )

# # except Exception as e:

# #     print(
# #         "Embedding model initialization error:",
# #         e
# #     )

# #     embedder = None


# # # ============================================================
# # # GENERATE ANSWER
# # # ============================================================

# # def generate_answer(
# #     prompt: str
# # ) -> str:

# #     # ========================================================
# #     # CLOUD LLM
# #     # ========================================================

# #     if (
# #         LLM_API_URL
# #         and LLM_API_KEY
# #         and LLM_MODEL
# #     ):

# #         headers = {

# #             "Authorization":
# #                 f"Bearer {LLM_API_KEY}",

# #             "Content-Type":
# #                 "application/json"
# #         }

# #         payload = {

# #             "model":
# #                 LLM_MODEL,

# #             "messages": [

# #                 {
# #                     "role":
# #                         "user",

# #                     "content":
# #                         prompt
# #                 }

# #             ],

# #             "temperature":
# #                 0.2
# #         }

# #         response = requests.post(
# #             LLM_API_URL,
# #             headers=headers,
# #             json=payload,
# #             timeout=120
# #         )

# #         response.raise_for_status()

# #         data = response.json()

# #         try:

# #             return (
# #                 data["choices"][0]
# #                 ["message"]["content"]
# #             ).strip()

# #         except (
# #             KeyError,
# #             IndexError,
# #             TypeError
# #         ):

# #             raise RuntimeError(
# #                 "Unexpected cloud LLM response format."
# #             )


# #     # ========================================================
# #     # OLLAMA
# #     # ========================================================

# #     if OLLAMA_URL:

# #         payload = {

# #             "model":
# #                 OLLAMA_MODEL,

# #             "prompt":
# #                 prompt,

# #             "stream":
# #                 False,

# #             "options": {

# #                 "temperature":
# #                     0.2
# #             }
# #         }

# #         response = requests.post(
# #             OLLAMA_URL,
# #             json=payload,
# #             timeout=180
# #         )

# #         response.raise_for_status()

# #         data = response.json()

# #         answer = data.get(
# #             "response",
# #             ""
# #         )

# #         if not answer:

# #             raise RuntimeError(
# #                 "Ollama returned an empty response."
# #             )

# #         return answer.strip()


# #     # ========================================================
# #     # NO LLM
# #     # ========================================================

# #     raise RuntimeError(
# #         "No LLM is configured."
# #     )


# # # ============================================================
# # # HOME
# # # ============================================================

# # @app.get("/")
# # def home():

# #     return {

# #         "message":
# #             "Sahayak backend is running",

# #         "status":
# #             "online",

# #         "service":
# #             "Sahayak API",

# #         "version":
# #             "1.0.0"
# #     }


# # # ============================================================
# # # HEALTH
# # # ============================================================

# # @app.get("/health")
# # def health():

# #     return {

# #         "status":
# #             "healthy",

# #         "qdrant":
# #             (
# #                 "connected"
# #                 if qdrant is not None
# #                 else "not_configured"
# #             ),

# #         "embedding_model":
# #             (
# #                 "loaded"
# #                 if embedder is not None
# #                 else "unavailable"
# #             ),

# #         "ollama":
# #             (
# #                 OLLAMA_MODEL
# #                 if OLLAMA_URL
# #                 else "not_configured"
# #             ),

# #         "cloud_llm":
# #             (
# #                 LLM_MODEL
# #                 if (
# #                     LLM_API_URL
# #                     and LLM_API_KEY
# #                     and LLM_MODEL
# #                 )
# #                 else "not_configured"
# #             )
# #     }


# # # ============================================================
# # # QUERY
# # # ============================================================

# # @app.post("/query")
# # def ask_sahayak(

# #     request: QueryRequest,

# #     current_user=Depends(
# #         get_current_user
# #     )
# # ):

# #     print(
# #         "\n=================================================="
# #     )

# #     print(
# #         "NEW SAHAYAK QUERY"
# #     )

# #     print(
# #         "Question:",
# #         request.query
# #     )

# #     print(
# #         "User:",
# #         current_user.get("email")
# #     )

# #     print(
# #         "=================================================="
# #     )


# #     # ========================================================
# #     # VALIDATE QUERY
# #     # ========================================================

# #     query = request.query.strip()


# #     if not query:

# #         raise HTTPException(
# #             status_code=400,
# #             detail=(
# #                 "Please enter a question."
# #             )
# #         )


# #     # ========================================================
# #     # VARIABLES
# #     # ========================================================

# #     results = []

# #     context_chunks = []

# #     highest_score = 0.0

# #     average_score = 0.0

# #     confidence = "Low"

# #     evidence_available = False

# #     retrieval_status = "not_attempted"


# #     # ========================================================
# #     # QDRANT RETRIEVAL
# #     # ========================================================

# #     if (
# #         qdrant is not None
# #         and embedder is not None
# #     ):

# #         try:

# #             embedding = embedder.encode(
# #                 query
# #             ).tolist()


# #             results = qdrant.query_points(

# #                 collection_name=
# #                     QDRANT_COLLECTION,

# #                 query=
# #                     embedding,

# #                 limit=5

# #             ).points


# #             retrieval_status = "success"


# #             print(
# #                 "Retrieved chunks:",
# #                 len(results)
# #             )


# #         except Exception as e:

# #             print(
# #                 "QDRANT RETRIEVAL ERROR:",
# #                 e
# #             )

# #             results = []

# #             retrieval_status = "failed"


# #     elif qdrant is None:

# #         retrieval_status = (
# #             "not_configured"
# #         )


# #     elif embedder is None:

# #         retrieval_status = (
# #             "embedding_unavailable"
# #         )


# #     # ========================================================
# #     # FILTER VALID EVIDENCE
# #     # ========================================================

# #     valid_results = [

# #         hit

# #         for hit in results

# #         if (
# #             hit.score is not None
# #             and hit.score >= RAG_SCORE_THRESHOLD
# #             and hit.payload
# #             and hit.payload.get("text")
# #         )
# #     ]


# #     # ========================================================
# #     # PROCESS SCORES
# #     # ========================================================

# #     if valid_results:

# #         scores = [

# #             hit.score

# #             for hit in valid_results

# #         ]


# #         highest_score = max(
# #             scores
# #         )

# #         average_score = (
# #             sum(scores)
# #             / len(scores)
# #         )


# #         # ====================================================
# #         # CONFIDENCE
# #         # ====================================================

# #         if (

# #             highest_score >= 0.70

# #             and average_score >= 0.55

# #         ):

# #             confidence = "High"


# #         elif (

# #             highest_score >= 0.55

# #             and average_score >= 0.40

# #         ):

# #             confidence = "Medium"


# #         else:

# #             confidence = "Low"


# #         # ====================================================
# #         # BUILD CONTEXT
# #         # ====================================================

# #         for i, hit in enumerate(
# #             valid_results,
# #             start=1
# #         ):

# #             payload = (
# #                 hit.payload
# #                 or {}
# #             )


# #             text = payload.get(
# #                 "text",
# #                 ""
# #             )


# #             context_chunks.append(

# #                 f"""
# # SOURCE {i}

# # Similarity Score:
# # {
# #     round(hit.score, 4)
# # }

# # Source Name:
# # {
# #     payload.get(
# #         "source_name",
# #         "Unknown"
# #     )
# # }

# # Organization:
# # {
# #     payload.get(
# #         "organization",
# #         "Unknown"
# #     )
# # }

# # Document:
# # {
# #     payload.get(
# #         "document_title",
# #         payload.get(
# #             "title",
# #             "Unknown"
# #         )
# #     )
# # }

# # Page / Section:
# # {
# #     payload.get(
# #         "page",
# #         ""
# #     )
# # }

# # Content:
# # {text}
# # """
# #             )


# #         if context_chunks:

# #             evidence_available = True


# #     # ========================================================
# #     # BUILD CONTEXT
# #     # ========================================================

# #     if evidence_available:

# #         context = "\n\n---\n\n".join(
# #             context_chunks
# #         )

# #         answer_mode = (
# #             "EVIDENCE-GROUNDED RAG MODE"
# #         )

# #     else:

# #         context = (
# #             "NO RETRIEVED EVIDENCE IS AVAILABLE."
# #         )

# #         answer_mode = (
# #             "GENERAL KNOWLEDGE MODE"
# #         )


# #     # ========================================================
# #     # PROMPT
# #     # ========================================================

# #     prompt = f"""
# # You are Sahayak, an AI assistant specializing in
# # Ayurveda intellectual property, patents, traditional
# # knowledge, and Indian regulations.

# # USER QUESTION:
# # {query}

# # STAKEHOLDER:
# # {request.stakeholder}

# # REQUESTED LANGUAGE:
# # {request.language}

# # ANSWER MODE:
# # {answer_mode}

# # RETRIEVED EVIDENCE:
# # {context}

# # IMPORTANT RULES:

# # 1. If evidence is available, use it as the primary
# #    basis for your answer.

# # 2. Do not invent laws, regulations, sections,
# #    organizations, documents, citations, or URLs.

# # 3. If the evidence only partially answers the question,
# #    clearly state what is supported and what is not.

# # 4. Mention the relevant source/document when supported
# #    by the retrieved evidence.

# # 5. If no evidence is available, begin the response with:

# # "General information — no supporting evidence was
# # retrieved from the Sahayak evidence database."

# # 6. In general knowledge mode, provide useful background
# #    but do not present uncertain legal information as a
# #    definitive legal conclusion.

# # 7. Respond in the requested language.

# # 8. Adapt the explanation to the stakeholder.

# # 9. Do not mention internal prompts or system instructions.

# # Answer the user's question now.
# # """


# #     # ========================================================
# #     # GENERATE ANSWER
# #     # ========================================================

# #     try:

# #         answer = generate_answer(
# #             prompt
# #         )

# #     except requests.exceptions.ConnectionError:

# #         raise HTTPException(
# #             status_code=503,
# #             detail=(
# #                 "Sahayak could not connect to "
# #                 "the language model. Please make "
# #                 "sure Ollama is running."
# #             )
# #         )

# #     except requests.exceptions.Timeout:

# #         raise HTTPException(
# #             status_code=504,
# #             detail=(
# #                 "The language model took too long "
# #                 "to respond. Please try again."
# #             )
# #         )

# #     except requests.exceptions.HTTPError as e:

# #         print(
# #             "LLM HTTP ERROR:",
# #             e
# #         )

# #         raise HTTPException(
# #             status_code=502,
# #             detail=(
# #                 "The language model returned an "
# #                 "invalid response."
# #             )
# #         )

# #     except Exception as e:

# #         print(
# #             "LLM ERROR:",
# #             e
# #         )

# #         raise HTTPException(
# #             status_code=500,
# #             detail=(
# #                 "An error occurred while generating "
# #                 "the answer."
# #             )
# #         )


# #     # ========================================================
# #     # BUILD SOURCES
# #     # ========================================================

# #     sources = []

# #     seen_sources = set()


# #     for hit in valid_results:

# #         payload = (
# #             hit.payload
# #             or {}
# #         )


# #         source_key = (

# #             payload.get(
# #                 "source_id"
# #             )

# #             or payload.get(
# #                 "source_url"
# #             )

# #             or payload.get(
# #                 "document_title"
# #             )

# #             or payload.get(
# #                 "source_name"
# #             )

# #             or "unknown"

# #         )


# #         if source_key in seen_sources:

# #             continue


# #         seen_sources.add(
# #             source_key
# #         )


# #         sources.append({

# #             "id":
# #                 len(sources) + 1,

# #             "source_name":
# #                 (
# #                     payload.get(
# #                         "source_name"
# #                     )

# #                     or payload.get(
# #                         "document_title"
# #                     )

# #                     or payload.get(
# #                         "organization"
# #                     )

# #                     or "Unknown Source"
# #                 ),

# #             "source_url":
# #                 payload.get(
# #                     "source_url",
# #                     ""
# #                 ),

# #             "document_title":
# #                 (
# #                     payload.get(
# #                         "document_title"
# #                     )

# #                     or payload.get(
# #                         "source_name"
# #                     )

# #                     or "Unknown Document"
# #                 ),

# #             "source_id":
# #                 payload.get(
# #                     "source_id",
# #                     ""
# #                 ),

# #             "organization":
# #                 payload.get(
# #                     "organization",
# #                     ""
# #                 ),

# #             "publication_date":
# #                 payload.get(
# #                     "publication_date",
# #                     ""
# #                 ),

# #             "page":
# #                 payload.get(
# #                     "page",
# #                     ""
# #                 ),

# #             "type":
# #                 payload.get(
# #                     "type",
# #                     "Legal Document"
# #                 ),

# #             "description":
# #                 payload.get(
# #                     "description",
# #                     ""
# #                 ),

# #             "similarity_score":
# #                 (
# #                     round(
# #                         hit.score,
# #                         4
# #                     )
# #                     if hit.score is not None
# #                     else None
# #                 )
# #         })


# #     # ========================================================
# #     # CONFIDENCE DETAILS
# #     # ========================================================

# #     if evidence_available:

# #         confidence_method = (
# #             "Based on Qdrant similarity scores "
# #             "from retrieved evidence."
# #         )

# #     else:

# #         confidence_method = (
# #             "No sufficiently relevant Qdrant evidence "
# #             "was available. Answer generated using "
# #             "Ollama general knowledge."
# #         )


# #     confidence_details = {

# #         "highest_score":
# #             round(
# #                 highest_score,
# #                 4
# #             ),

# #         "average_score":
# #             round(
# #                 average_score,
# #                 4
# #             ),

# #         "retrieved_chunks":
# #             len(valid_results),

# #         "retrieval_status":
# #             retrieval_status,

# #         "confidence_method":
# #             confidence_method
# #     }


# #     # ========================================================
# #     # SAVE CHAT
# #     # ========================================================

# #     chat_document = {

# #         "user_id":
# #             current_user["_id"],

# #         "user_email":
# #             current_user.get(
# #                 "email",
# #                 ""
# #             ),

# #         "query":
# #             query,

# #         "answer":
# #             answer.strip(),

# #         "language":
# #             request.language,

# #         "stakeholder":
# #             request.stakeholder,

# #         "sources":
# #             sources,

# #         "confidence":
# #             confidence,

# #         "confidence_details":
# #             confidence_details,

# #         "answer_mode":
# #             answer_mode,

# #         "created_at":
# #             datetime.now(
# #                 timezone.utc
# #             )
# #     }


# #     try:

# #         chat_result = (
# #             chats_collection.insert_one(
# #                 chat_document
# #             )
# #         )

# #         chat_id = str(
# #             chat_result.inserted_id
# #         )

# #     except Exception as e:

# #         print(
# #             "MongoDB chat save error:",
# #             e
# #         )

# #         # Do NOT fail the whole AI answer merely
# #         # because chat history could not be saved.

# #         chat_id = None


# #     # ========================================================
# #     # FINAL RESPONSE
# #     # ========================================================

# #     return {

# #         "chat_id":
# #             chat_id,

# #         "answer":
# #             answer.strip(),

# #         "sources":
# #             sources,

# #         "confidence":
# #             confidence,

# #         "confidence_details":
# #             confidence_details,

# #         "answer_mode":
# #             answer_mode
# #     }


# # # ============================================================
# # # GET ALL CHATS
# # # ============================================================

# # @app.get("/chats")
# # def get_chats(

# #     current_user=Depends(
# #         get_current_user
# #     )

# # ):

# #     try:

# #         chats = chats_collection.find(

# #             {
# #                 "user_id":
# #                     current_user["_id"]
# #             }

# #         ).sort(

# #             "created_at",
# #             -1
# #         )

# #     except Exception as e:

# #         print(
# #             "MongoDB error while fetching chats:",
# #             e
# #         )

# #         raise HTTPException(
# #             status_code=500,
# #             detail=(
# #                 "Unable to retrieve chat history."
# #             )
# #         )


# #     chat_list = []


# #     for chat in chats:

# #         chat_list.append({

# #             "id":
# #                 str(
# #                     chat["_id"]
# #                 ),

# #             "query":
# #                 chat.get(
# #                     "query",
# #                     ""
# #                 ),

# #             "answer":
# #                 chat.get(
# #                     "answer",
# #                     ""
# #                 ),

# #             "language":
# #                 chat.get(
# #                     "language",
# #                     "English"
# #                 ),

# #             "stakeholder":
# #                 chat.get(
# #                     "stakeholder",
# #                     "Researcher"
# #                 ),

# #             "confidence":
# #                 chat.get(
# #                     "confidence",
# #                     "Low"
# #                 ),

# #             "created_at":
# #                 chat.get(
# #                     "created_at"
# #                 ),

# #             "sources_count":
# #                 len(
# #                     chat.get(
# #                         "sources",
# #                         []
# #                     )
# #                 )
# #         })


# #     return {

# #         "chats":
# #             chat_list,

# #         "count":
# #             len(chat_list)
# #     }


# # # ============================================================
# # # GET SINGLE CHAT
# # # ============================================================

# # @app.get("/chats/{chat_id}")
# # def get_chat(

# #     chat_id: str,

# #     current_user=Depends(
# #         get_current_user
# #     )

# # ):

# #     # ========================================================
# #     # VALIDATE OBJECT ID
# #     # ========================================================

# #     try:

# #         object_id = ObjectId(
# #             chat_id
# #         )

# #     except Exception:

# #         raise HTTPException(
# #             status_code=400,
# #             detail=(
# #                 "Invalid chat ID."
# #             )
# #         )


# #     # ========================================================
# #     # FIND CHAT
# #     # ========================================================

# #     try:

# #         chat = chats_collection.find_one(

# #             {

# #                 "_id":
# #                     object_id,

# #                 "user_id":
# #                     current_user["_id"]
# #             }
# #         )

# #     except Exception as e:

# #         print(
# #             "MongoDB error while fetching chat:",
# #             e
# #         )

# #         raise HTTPException(
# #             status_code=500,
# #             detail=(
# #                 "Unable to retrieve chat."
# #             )
# #         )


# #     # ========================================================
# #     # NOT FOUND
# #     # ========================================================

# #     if not chat:

# #         raise HTTPException(
# #             status_code=404,
# #             detail=(
# #                 "Chat not found."
# #             )
# #         )


# #     # ========================================================
# #     # RESPONSE
# #     # ========================================================

# #     return {

# #         "id":
# #             str(
# #                 chat["_id"]
# #             ),

# #         "query":
# #             chat.get(
# #                 "query",
# #                 ""
# #             ),

# #         "answer":
# #             chat.get(
# #                 "answer",
# #                 ""
# #             ),

# #         "language":
# #             chat.get(
# #                 "language",
# #                 "English"
# #             ),

# #         "stakeholder":
# #             chat.get(
# #                 "stakeholder",
# #                 "Researcher"
# #             ),

# #         "sources":
# #             chat.get(
# #                 "sources",
# #                 []
# #             ),

# #         "confidence":
# #             chat.get(
# #                 "confidence",
# #                 "Low"
# #             ),

# #         "confidence_details":
# #             chat.get(
# #                 "confidence_details",
# #                 {}
# #             ),

# #         "answer_mode":
# #             chat.get(
# #                 "answer_mode",
# #                 "UNKNOWN"
# #             ),

# #         "created_at":
# #             chat.get(
# #                 "created_at"
# #             )
# #     }
# import os

# from datetime import datetime, timezone

# import requests

# from bson import ObjectId

# from dotenv import load_dotenv

# from fastapi import (
#     FastAPI,
#     Depends,
#     HTTPException
# )

# from fastapi.middleware.cors import CORSMiddleware

# from pydantic import BaseModel

# from qdrant_client import QdrantClient

# from sentence_transformers import SentenceTransformer

# from auth import (
#     router as auth_router,
#     get_current_user
# )

# from database import chats_collection


# # ============================================================
# # LOAD ENVIRONMENT
# # ============================================================

# load_dotenv()


# # ============================================================
# # FRONTEND
# # ============================================================

# FRONTEND_URL = os.getenv(
#     "FRONTEND_URL",
#     "http://localhost:5173"
# )


# # ============================================================
# # QDRANT CLOUD
# # ============================================================

# QDRANT_URL = os.getenv(
#     "CLOUD_QDRANT_URL",
#     ""
# )

# QDRANT_API_KEY = os.getenv(
#     "CLOUD_QDRANT_API_KEY",
#     ""
# )

# QDRANT_COLLECTION = os.getenv(
#     "QDRANT_COLLECTION",
#     "ayurveda_ip"
# )


# # ============================================================
# # GEMINI API
# # ============================================================

# GEMINI_API_KEY = os.getenv(
#     "GEMINI_API_KEY",
#     ""
# )

# GEMINI_MODEL = os.getenv(
#     "GEMINI_MODEL",
#     "gemini-2.5-flash"
# )

# GEMINI_API_URL = (
#     "https://generativelanguage.googleapis.com/"
#     "v1beta/models/"
#     f"{GEMINI_MODEL}:generateContent"
# )


# # ============================================================
# # RAG SETTINGS
# # ============================================================

# RAG_SCORE_THRESHOLD = float(
#     os.getenv(
#         "RAG_SCORE_THRESHOLD",
#         "0.45"
#     )
# )

# RAG_TOP_K = int(
#     os.getenv(
#         "RAG_TOP_K",
#         "5"
#     )
# )


# # ============================================================
# # FASTAPI
# # ============================================================

# app = FastAPI(
#     title="Sahayak API",

#     description=(
#         "AI Assistant for "
#         "Ayurveda IP & Regulation"
#     ),

#     version="1.0.0"
# )


# # ============================================================
# # CORS
# # ============================================================

# allowed_origins = [

#     FRONTEND_URL,

#     "http://localhost:5173",

#     "http://127.0.0.1:5173"
# ]


# allowed_origins = list(
#     dict.fromkeys(
#         origin.rstrip("/")
#         for origin in allowed_origins
#         if origin
#     )
# )


# app.add_middleware(

#     CORSMiddleware,

#     allow_origins=allowed_origins,

#     allow_credentials=True,

#     allow_methods=["*"],

#     allow_headers=["*"]
# )


# # ============================================================
# # AUTH ROUTER
# # ============================================================

# app.include_router(
#     auth_router
# )


# # ============================================================
# # REQUEST MODEL
# # ============================================================

# class QueryRequest(BaseModel):

#     query: str

#     language: str = "English"

#     stakeholder: str = "Researcher"


# # ============================================================
# # QDRANT INITIALIZATION
# # ============================================================

# qdrant = None


# if QDRANT_URL and QDRANT_API_KEY:

#     try:

#         qdrant = QdrantClient(

#             url=QDRANT_URL,

#             api_key=QDRANT_API_KEY,

#             check_compatibility=False
#         )

#         print(
#             "=================================================="
#         )

#         print(
#             "QDRANT: Connected to Qdrant Cloud"
#         )

#         print(
#             "Collection:",
#             QDRANT_COLLECTION
#         )

#         print(
#             "=================================================="
#         )

#     except Exception as e:

#         print(
#             "QDRANT INITIALIZATION ERROR:",
#             e
#         )

#         qdrant = None

# else:

#     print(
#         "=================================================="
#     )

#     print(
#         "QDRANT: Not configured"
#     )

#     print(
#         "=================================================="
#     )


# # ============================================================
# # VERIFY QDRANT COLLECTION
# # ============================================================

# if qdrant is not None:

#     try:

#         collections = qdrant.get_collections()

#         collection_names = [

#             collection.name

#             for collection in collections.collections
#         ]

#         if QDRANT_COLLECTION in collection_names:

#             print(
#                 f"QDRANT COLLECTION VERIFIED: "
#                 f"{QDRANT_COLLECTION}"
#             )

#         else:

#             print(
#                 "WARNING: Qdrant collection not found:",
#                 QDRANT_COLLECTION
#             )

#             print(
#                 "Available collections:",
#                 collection_names
#             )

#     except Exception as e:

#         print(
#             "QDRANT COLLECTION CHECK ERROR:",
#             e
#         )


# # ============================================================
# # EMBEDDING MODEL
# # ============================================================

# embedder = None


# try:

#     print(
#         "Loading embedding model..."
#     )

#     embedder = SentenceTransformer(
#         "all-MiniLM-L6-v2"
#     )

#     print(
#         "Embedding model loaded successfully."
#     )

# except Exception as e:

#     print(
#         "Embedding model initialization error:",
#         e
#     )

#     embedder = None


# # ============================================================
# # GEMINI INITIALIZATION CHECK
# # ============================================================

# if GEMINI_API_KEY:

#     print(
#         "=================================================="
#     )

#     print(
#         "GEMINI: Configured"
#     )

#     print(
#         "Model:",
#         GEMINI_MODEL
#     )

#     print(
#         "=================================================="
#     )

# else:

#     print(
#         "=================================================="
#     )

#     print(
#         "GEMINI: API key not configured"
#     )

#     print(
#         "Set GEMINI_API_KEY in .env"
#     )

#     print(
#         "=================================================="
#     )


# # ============================================================
# # GEMINI ANSWER GENERATION
# # ============================================================

# def generate_answer(
#     prompt: str
# ) -> str:

#     """
#     Generate an answer using Google Gemini API.

#     Ollama is NOT used.
#     """

#     if not GEMINI_API_KEY:

#         raise RuntimeError(
#             "Gemini API key is not configured. "
#             "Set GEMINI_API_KEY in .env."
#         )


#     headers = {

#         "Content-Type":
#             "application/json",

#         "x-goog-api-key":
#             GEMINI_API_KEY
#     }


#     payload = {

#         "contents": [

#             {

#                 "parts": [

#                     {
#                         "text": prompt
#                     }

#                 ]

#             }

#         ],

#         "generationConfig": {

#             "temperature":
#                 0.2
#         }

#     }


#     print(
#         "Generating answer with Gemini:",
#         GEMINI_MODEL
#     )


#     response = requests.post(

#         GEMINI_API_URL,

#         headers=headers,

#         json=payload,

#         timeout=120
#     )


#     if response.status_code != 200:

#         print(
#             "GEMINI ERROR STATUS:",
#             response.status_code
#         )

#         print(
#             "GEMINI ERROR RESPONSE:",
#             response.text
#         )


#     response.raise_for_status()


#     data = response.json()


#     try:

#         candidates = data.get(
#             "candidates",
#             []
#         )


#         if not candidates:

#             raise RuntimeError(
#                 "Gemini returned no candidates."
#             )


#         content = candidates[0].get(
#             "content",
#             {}
#         )


#         parts = content.get(
#             "parts",
#             []
#         )


#         answer_parts = [

#             part.get(
#                 "text",
#                 ""
#             )

#             for part in parts

#             if part.get("text")
#         ]


#         answer = "\n".join(
#             answer_parts
#         ).strip()


#         if not answer:

#             raise RuntimeError(
#                 "Gemini returned an empty response."
#             )


#         return answer


#     except (
#         KeyError,
#         IndexError,
#         TypeError
#     ) as e:

#         print(
#             "Unexpected Gemini response:",
#             data
#         )

#         raise RuntimeError(
#             "Unexpected Gemini response format."
#         ) from e


# # ============================================================
# # HOME
# # ============================================================

# @app.get("/")
# def home():

#     return {

#         "message":
#             "Sahayak backend is running",

#         "status":
#             "online",

#         "service":
#             "Sahayak API",

#         "version":
#             "1.0.0"
#     }


# # ============================================================
# # HEALTH
# # ============================================================

# @app.get("/health")
# def health():

#     return {

#         "status":
#             "healthy",

#         "qdrant":
#             (
#                 "connected"
#                 if qdrant is not None
#                 else "not_configured"
#             ),

#         "qdrant_collection":
#             QDRANT_COLLECTION,

#         "embedding_model":
#             (
#                 "loaded"
#                 if embedder is not None
#                 else "unavailable"
#             ),

#         "gemini":
#             (
#                 GEMINI_MODEL
#                 if GEMINI_API_KEY
#                 else "not_configured"
#             ),

#         "rag_threshold":
#             RAG_SCORE_THRESHOLD,

#         "rag_top_k":
#             RAG_TOP_K
#     }


# # ============================================================
# # QUERY
# # ============================================================

# @app.post("/query")
# def ask_sahayak(

#     request: QueryRequest,

#     current_user=Depends(
#         get_current_user
#     )

# ):

#     print(
#         "\n=================================================="
#     )

#     print(
#         "NEW SAHAYAK QUERY"
#     )

#     print(
#         "=================================================="
#     )

#     print(
#         "Question:",
#         request.query
#     )

#     print(
#         "Language:",
#         request.language
#     )

#     print(
#         "Stakeholder:",
#         request.stakeholder
#     )

#     print(
#         "User:",
#         current_user.get("email")
#     )


#     # ========================================================
#     # VALIDATE QUERY
#     # ========================================================

#     query = request.query.strip()


#     if not query:

#         raise HTTPException(

#             status_code=400,

#             detail=(
#                 "Please enter a question."
#             )
#         )


#     # ========================================================
#     # VARIABLES
#     # ========================================================

#     results = []

#     valid_results = []

#     context_chunks = []

#     highest_score = 0.0

#     average_score = 0.0

#     confidence = "Low"

#     evidence_available = False

#     retrieval_status = "not_attempted"


#     # ========================================================
#     # QDRANT RETRIEVAL
#     # ========================================================

#     if (

#         qdrant is not None

#         and embedder is not None

#     ):

#         try:

#             print(
#                 "Generating query embedding..."
#             )


#             embedding = embedder.encode(

#                 query

#             ).tolist()


#             print(
#                 "Searching Qdrant Cloud..."
#             )


#             results = qdrant.query_points(

#                 collection_name=
#                     QDRANT_COLLECTION,

#                 query=
#                     embedding,

#                 limit=
#                     RAG_TOP_K

#             ).points


#             retrieval_status = "success"


#             print(
#                 "Retrieved chunks:",
#                 len(results)
#             )


#             print(
#                 "Qdrant scores:",
#                 [
#                     round(
#                         hit.score,
#                         4
#                     )

#                     for hit in results

#                     if hit.score is not None
#                 ]
#             )


#         except Exception as e:

#             print(
#                 "QDRANT RETRIEVAL ERROR:",
#                 e
#             )

#             results = []

#             retrieval_status = "failed"


#     elif qdrant is None:

#         retrieval_status = (
#             "not_configured"
#         )


#     elif embedder is None:

#         retrieval_status = (
#             "embedding_unavailable"
#         )


#     # ========================================================
#     # FILTER VALID EVIDENCE
#     # ========================================================

#     valid_results = [

#         hit

#         for hit in results

#         if (

#             hit.score is not None

#             and hit.score >= RAG_SCORE_THRESHOLD

#             and hit.payload

#             and hit.payload.get("text")

#         )

#     ]


#     print(
#         "Valid evidence chunks:",
#         len(valid_results)
#     )


#     # ========================================================
#     # PROCESS SCORES
#     # ========================================================

#     if valid_results:

#         scores = [

#             hit.score

#             for hit in valid_results

#             if hit.score is not None

#         ]


#         if scores:

#             highest_score = max(
#                 scores
#             )

#             average_score = (

#                 sum(scores)

#                 / len(scores)

#             )


#         # ====================================================
#         # CONFIDENCE
#         # ====================================================

#         if (

#             highest_score >= 0.70

#             and average_score >= 0.55

#         ):

#             confidence = "High"


#         elif (

#             highest_score >= 0.55

#             and average_score >= 0.40

#         ):

#             confidence = "Medium"


#         else:

#             confidence = "Low"


#         # ====================================================
#         # BUILD CONTEXT
#         # ====================================================

#         for i, hit in enumerate(

#             valid_results,

#             start=1

#         ):

#             payload = (
#                 hit.payload
#                 or {}
#             )


#             text = payload.get(
#                 "text",
#                 ""
#             )


#             context_chunks.append(

#                 f"""
# SOURCE {i}

# Similarity Score:
# {
#     round(
#         hit.score,
#         4
#     )
# }

# Source Name:
# {
#     payload.get(
#         "source_name",
#         "Unknown"
#     )
# }

# Organization:
# {
#     payload.get(
#         "organization",
#         "Unknown"
#     )
# }

# Document:
# {
#     payload.get(
#         "document_title",
#         payload.get(
#             "title",
#             "Unknown"
#         )
#     )
# }

# Page / Section:
# {
#     payload.get(
#         "page",
#         ""
#     )
# }

# Content:
# {text}
# """

#             )


#         if context_chunks:

#             evidence_available = True


#     # ========================================================
#     # BUILD RAG CONTEXT
#     # ========================================================

#     if evidence_available:

#         context = "\n\n---\n\n".join(

#             context_chunks

#         )

#         answer_mode = (
#             "EVIDENCE-GROUNDED RAG MODE"
#         )

#     else:

#         context = (
#             "NO RETRIEVED EVIDENCE IS AVAILABLE."
#         )

#         answer_mode = (
#             "GENERAL KNOWLEDGE MODE"
#         )


#     # ========================================================
#     # GEMINI PROMPT
#     # ========================================================

#     prompt = f"""
# You are Sahayak, an AI assistant specializing in
# Ayurveda intellectual property, patents, traditional
# knowledge, and Indian regulations.

# Your job is to provide accurate, useful, and
# evidence-grounded answers.

# ============================================================
# USER QUESTION
# ============================================================

# {query}

# ============================================================
# STAKEHOLDER
# ============================================================

# {request.stakeholder}

# ============================================================
# REQUESTED LANGUAGE
# ============================================================

# {request.language}

# Supported languages:

# - English
# - Hindi
# - Marathi
# - Tamil

# ============================================================
# ANSWER MODE
# ============================================================

# {answer_mode}

# ============================================================
# RETRIEVED EVIDENCE FROM SAHAYAK DATABASE
# ============================================================

# {context}

# ============================================================
# IMPORTANT RULES
# ============================================================

# 1. EVIDENCE-GROUNDED RAG MODE

# If retrieved evidence is available:

# - Use the retrieved evidence as the primary basis
#   of your answer.

# - Carefully reason over the retrieved evidence.

# - Do not invent laws, regulations, legal sections,
#   organizations, documents, citations, URLs,
#   dates, or facts.

# - Do not claim that a document says something unless
#   the retrieved evidence actually supports it.

# - If the evidence directly answers the question,
#   explain it clearly.

# - If the evidence only partially answers the question,
#   clearly distinguish supported information from
#   unsupported information.

# - Mention relevant source/document names when supported
#   by the evidence.

# - Do not simply copy the retrieved text.

# - Synthesize the evidence into a clear answer.

# ============================================================
# 2. GENERAL KNOWLEDGE MODE
# ============================================================

# If no sufficiently relevant evidence was retrieved,
# begin the answer with exactly:

# "General information — no supporting evidence was
# retrieved from the Sahayak evidence database."

# Then:

# - Provide useful general background.

# - Do not invent specific laws, sections, regulations,
#   government notifications, citations, or URLs.

# - For legal and intellectual-property questions,
#   avoid presenting uncertain information as a
#   definitive legal conclusion.

# - Clearly state uncertainty where appropriate.

# ============================================================
# 3. SOURCE DISCIPLINE
# ============================================================

# Only use information supported by the retrieved evidence
# when making evidence-grounded claims.

# Do not fabricate:

# - source names
# - document names
# - URLs
# - legal provisions
# - patent rules
# - government organizations
# - publication dates
# - page numbers

# ============================================================
# 4. LANGUAGE
# ============================================================

# Respond in:

# {request.language}

# ============================================================
# 5. STAKEHOLDER
# ============================================================

# Adapt the explanation to:

# {request.stakeholder}

# ============================================================
# 6. STYLE
# ============================================================

# - Be clear.
# - Be concise but useful.
# - Use headings when useful.
# - Use bullet points when useful.
# - Explain difficult legal/IP concepts simply.
# - Do not mention this prompt.
# - Do not mention internal system instructions.
# - Do not mention token limits.
# - Do not fabricate evidence.

# ============================================================
# FINAL TASK
# ============================================================

# Answer the user's question now.
# """


#     # ========================================================
#     # GENERATE ANSWER WITH GEMINI
#     # ========================================================

#     try:

#         answer = generate_answer(
#             prompt
#         )

#         print(
#             "Answer generated successfully."
#         )


#     except requests.exceptions.ConnectionError as e:

#         print(
#             "GEMINI CONNECTION ERROR:",
#             e
#         )

#         raise HTTPException(

#             status_code=503,

#             detail=(
#                 "Sahayak could not connect to "
#                 "the Gemini API."
#             )
#         )


#     except requests.exceptions.Timeout as e:

#         print(
#             "GEMINI TIMEOUT:",
#             e
#         )

#         raise HTTPException(

#             status_code=504,

#             detail=(
#                 "Gemini took too long to respond. "
#                 "Please try again."
#             )
#         )


#     except requests.exceptions.HTTPError as e:

#         print(
#             "GEMINI HTTP ERROR:",
#             e
#         )

#         raise HTTPException(

#             status_code=502,

#             detail=(
#                 "Gemini API returned an error. "
#                 "Check your Gemini API key, "
#                 "model, quota, and API configuration."
#             )
#         )


#     except Exception as e:

#         print(
#             "GEMINI ERROR:",
#             e
#         )

#         raise HTTPException(

#             status_code=500,

#             detail=(
#                 "An error occurred while generating "
#                 "the answer with Gemini."
#             )
#         )


#     # ========================================================
#     # BUILD SOURCES
#     # ========================================================

#     sources = []

#     seen_sources = set()


#     for hit in valid_results:

#         payload = (
#             hit.payload
#             or {}
#         )


#         source_key = (

#             payload.get(
#                 "source_id"
#             )

#             or payload.get(
#                 "source_url"
#             )

#             or payload.get(
#                 "document_title"
#             )

#             or payload.get(
#                 "source_name"
#             )

#             or "unknown"

#         )


#         if source_key in seen_sources:

#             continue


#         seen_sources.add(
#             source_key
#         )


#         sources.append({

#             "id":
#                 len(sources) + 1,

#             "source_name":
#                 (
#                     payload.get(
#                         "source_name"
#                     )

#                     or payload.get(
#                         "document_title"
#                     )

#                     or payload.get(
#                         "organization"
#                     )

#                     or "Unknown Source"
#                 ),

#             "source_url":
#                 payload.get(
#                     "source_url",
#                     ""
#                 ),

#             "document_title":
#                 (
#                     payload.get(
#                         "document_title"
#                     )

#                     or payload.get(
#                         "source_name"
#                     )

#                     or "Unknown Document"
#                 ),

#             "source_id":
#                 payload.get(
#                     "source_id",
#                     ""
#                 ),

#             "organization":
#                 payload.get(
#                     "organization",
#                     ""
#                 ),

#             "publication_date":
#                 payload.get(
#                     "publication_date",
#                     ""
#                 ),

#             "page":
#                 payload.get(
#                     "page",
#                     ""
#                 ),

#             "type":
#                 payload.get(
#                     "type",
#                     "Legal Document"
#                 ),

#             "description":
#                 payload.get(
#                     "description",
#                     ""
#                 ),

#             "similarity_score":
#                 (
#                     round(
#                         hit.score,
#                         4
#                     )

#                     if hit.score is not None

#                     else None
#                 )
#         })


#     # ========================================================
#     # CONFIDENCE DETAILS
#     # ========================================================

#     if evidence_available:

#         confidence_method = (

#             "Based on Qdrant similarity scores "
#             "from retrieved evidence."
#         )

#     else:

#         confidence_method = (

#             "No sufficiently relevant Qdrant evidence "
#             "was available. Answer generated using "
#             "Gemini general knowledge."
#         )


#     confidence_details = {

#         "highest_score":
#             round(
#                 highest_score,
#                 4
#             ),

#         "average_score":
#             round(
#                 average_score,
#                 4
#             ),

#         "retrieved_chunks":
#             len(valid_results),

#         "retrieval_status":
#             retrieval_status,

#         "confidence_method":
#             confidence_method
#     }


#     # ========================================================
#     # SAVE CHAT TO MONGODB
#     # ========================================================

#     chat_document = {

#         "user_id":
#             current_user["_id"],

#         "user_email":
#             current_user.get(
#                 "email",
#                 ""
#             ),

#         "query":
#             query,

#         "answer":
#             answer.strip(),

#         "language":
#             request.language,

#         "stakeholder":
#             request.stakeholder,

#         "sources":
#             sources,

#         "confidence":
#             confidence,

#         "confidence_details":
#             confidence_details,

#         "answer_mode":
#             answer_mode,

#         "created_at":
#             datetime.now(
#                 timezone.utc
#             )
#     }


#     chat_id = None


#     try:

#         chat_result = (
#             chats_collection.insert_one(
#                 chat_document
#             )
#         )


#         chat_id = str(
#             chat_result.inserted_id
#         )


#         print(
#             "Chat saved:",
#             chat_id
#         )


#     except Exception as e:

#         print(
#             "MongoDB chat save error:",
#             e
#         )

#         # Chat history failure should not
#         # break the AI response.

#         chat_id = None


#     # ========================================================
#     # FINAL RESPONSE
#     # ========================================================

#     return {

#         "chat_id":
#             chat_id,

#         "answer":
#             answer.strip(),

#         "sources":
#             sources,

#         "confidence":
#             confidence,

#         "confidence_details":
#             confidence_details,

#         "answer_mode":
#             answer_mode
#     }


# # ============================================================
# # GET ALL CHATS
# # ============================================================

# @app.get("/chats")
# def get_chats(

#     current_user=Depends(
#         get_current_user
#     )

# ):

#     try:

#         chats = chats_collection.find(

#             {
#                 "user_id":
#                     current_user["_id"]
#             }

#         ).sort(

#             "created_at",
#             -1
#         )


#         chat_list = []


#         for chat in chats:

#             chat_list.append({

#                 "id":
#                     str(
#                         chat["_id"]
#                     ),

#                 "query":
#                     chat.get(
#                         "query",
#                         ""
#                     ),

#                 "answer":
#                     chat.get(
#                         "answer",
#                         ""
#                     ),

#                 "language":
#                     chat.get(
#                         "language",
#                         "English"
#                     ),

#                 "stakeholder":
#                     chat.get(
#                         "stakeholder",
#                         "Researcher"
#                     ),

#                 "confidence":
#                     chat.get(
#                         "confidence",
#                         "Low"
#                     ),

#                 "created_at":
#                     chat.get(
#                         "created_at"
#                     ),

#                 "sources_count":
#                     len(
#                         chat.get(
#                             "sources",
#                             []
#                         )
#                     )
#             })


#         return {

#             "chats":
#                 chat_list,

#             "count":
#                 len(chat_list)
#         }


#     except Exception as e:

#         print(
#             "MongoDB error while fetching chats:",
#             e
#         )

#         raise HTTPException(

#             status_code=500,

#             detail=(
#                 "Unable to retrieve chat history."
#             )
#         )


# # ============================================================
# # GET SINGLE CHAT
# # ============================================================

# @app.get("/chats/{chat_id}")
# def get_chat(

#     chat_id: str,

#     current_user=Depends(
#         get_current_user
#     )

# ):

#     # ========================================================
#     # VALIDATE OBJECT ID
#     # ========================================================

#     try:

#         object_id = ObjectId(
#             chat_id
#         )

#     except Exception:

#         raise HTTPException(

#             status_code=400,

#             detail=(
#                 "Invalid chat ID."
#             )
#         )


#     # ========================================================
#     # FIND CHAT
#     # ========================================================

#     try:

#         chat = chats_collection.find_one(

#             {

#                 "_id":
#                     object_id,

#                 "user_id":
#                     current_user["_id"]
#             }
#         )


#     except Exception as e:

#         print(
#             "MongoDB error while fetching chat:",
#             e
#         )

#         raise HTTPException(

#             status_code=500,

#             detail=(
#                 "Unable to retrieve chat."
#             )
#         )


#     # ========================================================
#     # CHAT NOT FOUND
#     # ========================================================

#     if not chat:

#         raise HTTPException(

#             status_code=404,

#             detail=(
#                 "Chat not found."
#             )
#         )


#     # ========================================================
#     # RESPONSE
#     # ========================================================

#     return {

#         "id":
#             str(
#                 chat["_id"]
#             ),

#         "query":
#             chat.get(
#                 "query",
#                 ""
#             ),

#         "answer":
#             chat.get(
#                 "answer",
#                 ""
#             ),

#         "language":
#             chat.get(
#                 "language",
#                 "English"
#             ),

#         "stakeholder":
#             chat.get(
#                 "stakeholder",
#                 "Researcher"
#             ),

#         "sources":
#             chat.get(
#                 "sources",
#                 []
#             ),

#         "confidence":
#             chat.get(
#                 "confidence",
#                 "Low"
#             ),

#         "confidence_details":
#             chat.get(
#                 "confidence_details",
#                 {}
#             ),

#         "answer_mode":
#             chat.get(
#                 "answer_mode",
#                 "UNKNOWN"
#             ),

#         "created_at":
#             chat.get(
#                 "created_at"
#             )
#     }
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
        print("Loading embedding model...")

        embedder = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully.")

    return embedder
# embedder = None


# try:

#     print(
#         "Loading embedding model..."
#     )

#     embedder = SentenceTransformer(
#         "all-MiniLM-L6-v2"
#     )

#     print(
#         "Embedding model loaded successfully."
#     )

# except Exception as e:

#     print(
#         "Embedding model initialization error:",
#         e
#     )

#     embedder = None


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


    # ========================================================
    # QDRANT RETRIEVAL
    # ========================================================
    if qdrant is not None:

        try:

            print(
                "Generating query embedding..."
            )

            embedding = get_embedder().encode(
                query
            ).tolist()

            print(
                "Searching Qdrant..."
            )

            results = qdrant.query_points(
                collection_name=QDRANT_COLLECTION,
                query=embedding,
                limit=TOP_K
            ).points

            retrieval_status = "success"

            print(
                "Retrieved chunks:",
                len(results)
            )

        except Exception as e:

            print(
                "QDRANT RETRIEVAL ERROR:",
                e
            )

            results = []

            retrieval_status = "failed"

    elif qdrant is None:

        retrieval_status = "not_configured"

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