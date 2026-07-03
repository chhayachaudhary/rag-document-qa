from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWTError
import os
from app.models.qa import QARequest, QAResponse
from app.services.vector_store import search_all_chunks
from app.services.llm import ask_llm

router = APIRouter(prefix="/qa", tags=["Q&A"])

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return email
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

@router.post("/ask", response_model=QAResponse)
def ask_question(request: QARequest, current_user: str = Depends(get_current_user)):
    chunks = search_all_chunks(request.question, request.filenames) if request.filenames else []

    answer = ask_llm(request.question, chunks)

    return QAResponse(
        question=request.question,
        answer=answer,
        source_chunks=chunks
    )
