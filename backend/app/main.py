from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.chain import ask_question
from app.rag.retriever import create_vector_store, get_vector_store

app = FastAPI(
    title="DevOpsRAG API",
    description="RAG-based DevOps Troubleshooting Assistant",
    version="0.1.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.on_event("startup")
def startup_event():

    print("Checking RAG vector database...")

    vector_store = get_vector_store()

    count = vector_store._collection.count()

    print(f"Existing vector documents: {count}")

    if count == 0:
        print("Vector database is empty.")
        print("Creating vector database...")

        create_vector_store()

        print("Vector database created successfully.")

    else:
        print("Vector database already exists.")



@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(request: QuestionRequest):
    return ask_question(request.question)
