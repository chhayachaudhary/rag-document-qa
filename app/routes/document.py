from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document import extract_text_from_pdf, chunk_text
from app.models.document import DocumentUploadResponse
from app.services.vector_store import store_chunks


router =APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model= DocumentUploadResponse)
async def upload_document(file: UploadFile= File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only Pdf files are supported")
    
    file_bytes= await file.read()
    extracted_text= extract_text_from_pdf(file_bytes)
    chunks = chunk_text(extracted_text)
    num_chunks = store_chunks(chunks, file.filename)

    return DocumentUploadResponse(
        filename=file.filename,
        message="Document processed successfully",
        chunks_created=num_chunks 
    )


       



