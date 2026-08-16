from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.chain import ask_question


app = FastAPI(
    title="DevOpsRAG API",
    description="RAG-based DevOps Troubleshooting Assistant",
    version="0.1.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "DevOpsRAG API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(request: QuestionRequest):
    return ask_question(request.question)
