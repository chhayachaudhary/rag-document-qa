# RAG Document Q&A — Backend

> The backend API for the RAG Document Q&A system. Built with FastAPI, this service handles user authentication, PDF document ingestion, vector embedding, semantic search and LLM-powered question answering.

🔗 **Frontend Repository:** [rag-document-qa-ui](https://github.com/chhayachaudhary/rag-document-qa-ui)  
🚀 **Live API:** [https://rag-document-qa-production-b719.up.railway.app](https://rag-document-qa-production-b719.up.railway.app)

---

## What is this project?

This is the backend of a full-stack AI application where users can:
- Register and log in securely
- Upload PDF documents
- Ask natural language questions about those documents
- Get AI-generated answers based only on the content of their uploaded documents

This backend follows a **decoupled architecture** — it is completely independent of the frontend. It exposes a REST API that any frontend (or client) can consume. The frontend lives in a separate repository.

---

## Architecture Overview

```
User uploads PDF
      ↓
Extract text (pypdf)
      ↓
Split into chunks
      ↓
Generate embeddings (sentence-transformers: all-MiniLM-L6-v2)
      ↓
Store in ChromaDB (vector database)
      ↓
User asks a question
      ↓
Search ChromaDB for relevant chunks (semantic similarity)
      ↓
Send question + context chunks to LLM (Groq: llama-3.3-70b-versatile)
      ↓
Return AI-generated answer
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Language | Python 3.11 |
| Authentication | JWT (PyJWT) + bcrypt |
| Database | SQLite via SQLAlchemy |
| Vector Store | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | Groq API (llama-3.3-70b-versatile) |
| PDF Parsing | pypdf |
| Deployment | Railway |

---

## Project Structure

```
RAG-Document-QA/
├── app/
│   ├── models/
│   │   ├── user.py         # User DB model + Pydantic schemas
│   │   ├── document.py     # Document upload response schema
│   │   └── qa.py           # Q&A request/response schemas
│   ├── routes/
│   │   ├── auth.py         # /auth/register, /auth/login
│   │   ├── document.py     # /documents/upload
│   │   └── qa.py           # /qa/ask
│   ├── services/
│   │   ├── auth.py         # JWT creation, password hashing, login/register logic
│   │   ├── document.py     # PDF text extraction and chunking
│   │   ├── vector_store.py # ChromaDB store and semantic search
│   │   └── llm.py          # Groq LLM integration
│   └── database.py         # SQLAlchemy engine and session setup
├── main.py                 # FastAPI app entry point, CORS config
├── requirements.txt
└── railway.toml            # Railway deployment config
```

---

## Authentication — How it works

This project uses **JWT (JSON Web Tokens)** for stateless authentication.

1. User registers with email and password
2. Password is hashed using `bcrypt` before storing in the database — plain passwords are never stored
3. On login, the password is verified against the hash
4. If valid, a JWT token is generated and signed with a `SECRET_KEY`
5. The token is returned to the frontend and stored in `localStorage`
6. Every protected request (like `/qa/ask`) must include the token in the `Authorization` header as `Bearer <token>`
7. The backend decodes and verifies the token on every protected request — if invalid or expired, it returns `401 Unauthorized`

---

## RAG Pipeline — How it works

**RAG = Retrieval Augmented Generation**

Instead of asking the LLM to answer from its training data, we:
1. Extract text from the uploaded PDF using `pypdf`
2. Split the text into overlapping chunks (500 chars, 50 char overlap)
3. Convert each chunk into a vector embedding using `sentence-transformers`
4. Store those embeddings in `ChromaDB` (a local vector database)
5. When a question is asked, convert the question into an embedding
6. Search ChromaDB for the most semantically similar chunks
7. Pass those chunks as context to the Groq LLM
8. The LLM answers based ONLY on that context

This means the AI answers are grounded in your actual documents, not hallucinated.

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |

### Documents
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/documents/upload` | Upload a PDF document | No |

### Q&A
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/qa/ask` | Ask a question about uploaded documents | Yes |

---

## Environment Variables

Create a `.env` file in the root:

```
SECRET_KEY=your_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GROQ_API_KEY=your_groq_api_key
FRONTEND_URL=https://rag-document-qa-ui.vercel.app
```

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/chhayachaudhary/rag-document-qa.git
cd rag-document-qa

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your .env file (see above)

# Start the server
uvicorn main:app --reload
```

API will be running at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

---

## Deployment

This backend is deployed on **Railway** using `railway.toml`.  
Railway automatically reads environment variables set in the service's Variables tab.

---

## Related

- 🖥️ Frontend: [rag-document-qa-ui](https://github.com/chhayachaudhary/rag-document-qa-ui)
