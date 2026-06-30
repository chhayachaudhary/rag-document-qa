from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.auth import router as auth_router
from app.database import engine, Base
from app.models.user import User
import os

load_dotenv()

# Creates all tables defined in models (only if they don't exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RAG Document Q&A",
    description="Upload your document and ask questions using AI.",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "RAG Document Q&A API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}