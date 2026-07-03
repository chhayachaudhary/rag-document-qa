from pydantic import BaseModel

class QARequest(BaseModel):
    question: str
    filenames: list[str]

class QAResponse(BaseModel):
    question: str
    answer: str
    source_chunks: list[str]


