from pypdf import PdfReader
import io

def extract_text_from_pdf(file_bytes: bytes)-> str:
    pdf_reader= PdfReader(io.BytesIO(file_bytes))
    text=""
    for page in pdf_reader.pages:
        text +=page.extract_text() + "\n"
    return text
     
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        if chunk.strip():  # skip empty chunks
            chunks.append(chunk)
        
        start = end - overlap  # move back by overlap amount

    return chunks