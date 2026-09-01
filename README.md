🌿 Sahayak RAG
AI-Powered Multilingual Assistant for Ayurveda, Traditional Knowledge & Intellectual Property

Sahayak RAG is a Retrieval-Augmented Generation (RAG) system that helps researchers, students, and stakeholders explore Indian traditional knowledge, Ayurveda documentation, and intellectual-property regulations. It delivers grounded answers with official sources in multiple languages.

✨ Why Sahayak?


🔎 Evidence-based: Answers are grounded in curated documents, not just model memory.

🌐 Multilingual: Supports English, Hindi, Marathi, and Tamil.

📚 Domain-focused: Built for Ayurveda, IP law, and traditional knowledge.

⚡ Cloud-ready: Frontend, backend, and vector DB deployed independently.

🛡️ Secure: JWT authentication, MongoDB Atlas, environment-variable secrets.

🏗️ Architecture
Code
React + Vite (Frontend) → Vercel
FastAPI (Backend) → Render
Qdrant Cloud (Vector DB)
MongoDB Atlas (User/Auth Data)
Gemini 3.6 Flash (LLM)
Workflow:
Query → Embedding → Qdrant Retrieval → Context → LLM → Grounded Answer + Sources

🚀 Features
Semantic Search: Uses sentence-transformers/all-MiniLM-L6-v2 for embeddings.

Source Registry: Every chunk linked to official source (IP India, AYUSH, WIPO, TKDL).

Evidence Cards: UI shows source name, type, page, and official URL.

Authentication: User login/registration with JWT + bcrypt.

Cloud Deployment: Fully deployed stack with shareable demo link.

⚙️ Local Setup
Backend

bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
Backend runs at: http://localhost:8000  
Docs: http://localhost:8000/docs

Frontend

bash
cd frontend
npm install
npm run dev
Frontend runs at: http://localhost:5173

🔐 Environment Variables
Create .env in backend/:

Code
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DATABASE=sahayak
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=ayurveda_ip
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET=your_secure_secret
🎯 Target Users
Researchers & academics

Ayurveda stakeholders

IP/legal researchers

Organizations working with traditional knowledge

🌍 SIH Relevance
Sahayak aligns with Smart India Hackathon goals by combining:
🇮🇳 Indian traditional knowledge corpus
🤖 Generative AI + RAG
📚 Evidence-oriented answers
🌐 Multilingual accessibility
☁️ Cloud deployment

📊 Future Scope
More authoritative sources (AYUSH, TKDL, WIPO)

Advanced citation tracing

Role-specific workflows

Retrieval evaluation & analytics

👥 Team
Add team members, college, department, mentor, and SIH problem statement ID here.
