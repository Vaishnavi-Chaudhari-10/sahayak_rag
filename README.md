🌿 Sahayak RAG

AI-Powered Multilingual Assistant for Ayurveda, Traditional Knowledge & Intellectual Property









Sahayak RAG is a multilingual Retrieval-Augmented Generation (RAG) assistant designed to help researchers and other stakeholders explore Indian traditional knowledge, Ayurveda documentation, intellectual-property concepts, and related regulatory information using grounded, source-aware responses.

📌 Problem Statement

Indian traditional knowledge and Ayurveda-related information is distributed across large collections of documents, regulations, publications, and intellectual-property resources. Finding relevant information manually can be time-consuming, while generic AI systems may produce answers without showing the evidence behind them.

Sahayak RAG addresses this problem by combining:

Document retrieval

Semantic vector search

Large Language Model (LLM) generation

Source-grounded responses

Multilingual interaction

User authentication and persistent user data

The goal is to make relevant information easier to discover, understand, and verify.

💡 What Makes Sahayak Different?

Sahayak is not designed as a simple chatbot.

It follows a retrieve → ground → generate workflow:

User Query
    ↓
Language / Query Processing
    ↓
Semantic Retrieval
    ↓
Qdrant Vector Database
    ↓
Relevant Knowledge Chunks
    ↓
LLM Context Construction
    ↓
LLM Response Generation
    ↓
Grounded Answer + Sources

This reduces the dependence on the model's internal knowledge and helps the system answer using the project's curated knowledge base.

✨ Key Features

🔎 Retrieval-Augmented Generation

Converts knowledge documents into searchable vector representations.

Retrieves semantically relevant chunks for each user query.

Uses retrieved context while generating the final response.

📚 Source-Grounded Answers

Responses are based on retrieved knowledge rather than relying only on free-form generation.

Relevant evidence/sources can be surfaced with the answer.

🌐 Multilingual Interaction

The application is designed for multilingual users, with support for:

English

Hindi

Marathi

Tamil

🧠 AI-Powered Assistance

The backend uses an LLM to synthesize retrieved information into understandable responses.

Current production configuration uses:

Gemini 3.6 Flash

👤 User Authentication

User registration/login functionality

Authentication-related data stored in MongoDB Atlas

Backend authentication implemented with JWT and password hashing

🗄️ Persistent Database

MongoDB Atlas is used for application data such as authentication/user information.

⚡ Cloud Vector Search

Qdrant Cloud stores and searches document embeddings.

Current collection:

ayurveda_ip

🚀 Cloud Deployment

The system is split into independently deployable frontend and backend services:

React + Vite  →  Vercel
FastAPI       →  Render
Qdrant        →  Qdrant Cloud
MongoDB       →  MongoDB Atlas
LLM           →  Gemini API

🏗️ System Architecture

                         ┌──────────────────────┐
                         │      User / UI       │
                         │   React + Vite       │
                         └──────────┬───────────┘
                                    │
                              HTTP / REST
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         │       Render         │
                         └───────┬───────┬──────┘
                                 │       │
                    ┌────────────┘       └──────────────┐
                    ▼                                   ▼
          ┌──────────────────┐                 ┌──────────────────┐
          │   Qdrant Cloud   │                 │  MongoDB Atlas   │
          │  ayurveda_ip     │                 │ Users / Auth     │
          │ Vector Retrieval  │                 │ Application Data │
          └────────┬─────────┘                 └──────────────────┘
                   │
                   │ Retrieved Context
                   ▼
          ┌──────────────────┐
          │   Gemini API     │
          │ Gemini 3.6 Flash │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Grounded Answer  │
          │ + Source Evidence│
          └──────────────────┘

🔄 RAG Pipeline

1. Document Ingestion

Source documents are collected and prepared for the knowledge base.

Documents
   ↓
Text Extraction
   ↓
Cleaning
   ↓
Chunking

2. Embedding Generation

Each chunk is converted into a numerical vector representation using:

sentence-transformers/all-MiniLM-L6-v2

3. Vector Storage

The generated embeddings and associated metadata are stored in Qdrant Cloud.

Collection: ayurveda_ip

4. Query Processing

When a user submits a question:

User Question
     ↓
Query Embedding
     ↓
Qdrant Similarity Search
     ↓
Top Relevant Chunks

5. Context-Aware Generation

Retrieved chunks are supplied as context to the LLM.

Retrieved Evidence
        +
User Question
        ↓
Gemini 3.6 Flash
        ↓
Final Answer

This architecture allows Sahayak to combine the search capability of a vector database with the language and reasoning capability of an LLM.

🧰 Technology Stack

Layer

Technology

Frontend

React + Vite

Backend

Python + FastAPI

Vector Database

Qdrant Cloud

Embeddings

sentence-transformers/all-MiniLM-L6-v2

LLM

Gemini 3.6 Flash

Application Database

MongoDB Atlas

Authentication

JWT + bcrypt

Document Processing

PyMuPDF, pypdf, BeautifulSoup

Data Processing

Pandas, NumPy

ML / Retrieval Utilities

scikit-learn, FAISS

API Server

Uvicorn

Frontend Deployment

Vercel

Backend Deployment

Render

📂 Project Structure

sahayak-rag/
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── ...
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   ├── raw/
│   ├── clean/
│   └── ...
│
├── scripts/
│   └── ...
│
├── requirements.txt
├── .gitignore
└── README.md

The exact contents of the repository may evolve as the project continues to be developed.

⚙️ Local Setup

Prerequisites

Make sure the following are installed:

Python 3.11+

Node.js

npm

Git

MongoDB Atlas account

Qdrant Cloud account

Gemini API access

1. Clone the Repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd sahayak-rag

2. Backend Setup

Create and activate a virtual environment:

Windows

python -m venv venv
venv\Scripts\activate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the backend locally:

uvicorn backend.main:app --reload --port 8000

The FastAPI API will be available locally at:

http://localhost:8000

FastAPI documentation:

http://localhost:8000/docs

🔐 Environment Variables

Create a .env file for local development.

Example:

MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DATABASE=sahayak

QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=ayurveda_ip

GEMINI_API_KEY=your_gemini_api_key

JWT_SECRET=your_secure_secret

Never commit .env, API keys, database passwords, JWT secrets, or other credentials to GitHub.

For production, configure these values using the hosting platform's environment-variable settings.

🎨 Frontend Setup

Move into the frontend directory:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The Vite development server will normally run on:

http://localhost:5173

Configure the frontend to use the deployed or local FastAPI backend through the application's API configuration.

🔌 API

The backend exposes REST APIs through FastAPI.

Main Query Endpoint

POST /query

Example request:

{
  "query": "Can a traditional Ayurvedic formulation be patented?",
  "language": "English",
  "stakeholder": "Researcher"
}

The endpoint processes the query through the retrieval and generation pipeline and returns the generated response along with relevant response/source information.

API Documentation

When the backend is running, interactive API documentation is available through:

/docs

☁️ Production Deployment

Backend — Render

The FastAPI backend is deployed on Render.

Production start command:

cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT

The deployed backend is currently live at:

https://sahayak-backend-vz96.onrender.com

Production services successfully verified during deployment:

✓ Uvicorn server started
✓ MongoDB Atlas connected
✓ Database: sahayak
✓ Qdrant Cloud connected
✓ Collection: ayurveda_ip verified
✓ Gemini configured
✓ Render service live

Frontend — Vercel

The React + Vite frontend is deployed separately on Vercel.

The frontend communicates with the FastAPI backend through HTTP requests.

🔒 Security Considerations

Sahayak uses several security-related practices:

Secrets are stored as environment variables.

MongoDB Atlas is used for managed database access.

Passwords are protected using bcrypt hashing.

JWT is used for authentication.

CORS is configured for the deployed frontend.

Database and API credentials are excluded from source control.

For production deployment, database network access should be configured to allow the backend service to connect securely.

🧪 Verification & Testing

The deployment process verifies the major infrastructure components before the application is served:

Application startup
        ↓
MongoDB connection
        ↓
Qdrant connection
        ↓
Collection verification
        ↓
LLM configuration
        ↓
FastAPI server
        ↓
Production service

This helps identify configuration failures early rather than allowing the application to start with unavailable dependencies.

📊 Why RAG?

A conventional LLM chatbot may generate an answer from its pretrained knowledge.

Sahayak instead follows:

Question
   ↓
Retrieve relevant evidence
   ↓
Provide evidence to LLM
   ↓
Generate grounded response

Benefits

Conventional Chatbot

Sahayak RAG

Relies mainly on model knowledge

Retrieves project-specific knowledge

Difficult to trace information

Can expose retrieved evidence

Knowledge can become outdated

Knowledge base can be updated

Generic responses

Domain-focused responses

Limited control over source corpus

Curated retrieval corpus

🎯 Target Users

Sahayak is intended to assist users such as:

🔬 Researchers

📚 Students and academics

⚖️ IP / legal-information researchers

🌿 Ayurveda and traditional-knowledge stakeholders

🏛️ Organizations working with Indian traditional knowledge documentation

Sahayak is an information-assistance system and should not be treated as a substitute for professional legal advice.

🌍 SIH Relevance

Sahayak aligns with the goals of a Smart India Hackathon solution by combining:

🇮🇳 Indian traditional knowledge and Ayurveda-focused information

🤖 Generative AI

🔎 Retrieval-Augmented Generation

🌐 Multilingual accessibility

📚 Evidence-oriented information retrieval

☁️ Cloud deployment

🔐 User authentication

🗄️ Persistent data storage

🧩 Modular and scalable architecture

The system is designed to turn a large and difficult-to-search document collection into an accessible conversational knowledge interface.

🚀 Future Scope

Potential extensions include:

Improved multilingual retrieval and generation

More government and authoritative knowledge sources

Better citation and evidence presentation

Advanced document-level source tracing

Improved retrieval evaluation and ranking

Role-specific workflows for different stakeholders

Analytics and feedback-driven retrieval improvement

Additional deployment and scalability optimizations

👥 Team

Project: Sahayak RAG
Focus: AI + RAG + Indian Traditional Knowledge + Ayurveda + IP
Hackathon: Smart India Hackathon (SIH)

Add your team member names, college, department, guide/mentor, and SIH problem statement ID here before the final SIH submission.

📜 License

Add the license selected by your team/institution here.

⭐ Acknowledgement

Sahayak RAG was developed as an applied AI project focused on making domain-specific information more searchable, accessible, multilingual, and evidence-oriented through Retrieval-Augmented Generation.
