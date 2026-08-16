import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.rag.embeddings import get_embedding_model
from app.rag.loader import load_documents
from app.rag.splitter import split_documents


PROJECT_ROOT = Path(
    os.getenv(
        "PROJECT_ROOT",
        str(Path(__file__).resolve().parents[3])
    )
)

DATA_PATH = PROJECT_ROOT / "data"
VECTOR_DB_PATH = PROJECT_ROOT / "vectorstore"


def create_vector_store():

    print(f"Loading documents from: {DATA_PATH}")

    documents = load_documents(str(DATA_PATH))

    print(f"Documents found: {len(documents)}")

    if not documents:
        raise ValueError(
            f"No documents found in {DATA_PATH}"
        )

    chunks = split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    if not chunks:
        raise ValueError(
            "No chunks were created from the documents."
        )

    langchain_documents = [
        Document(
            page_content=chunk["content"],
            metadata={
                "source": chunk["source"]
            }
        )
        for chunk in chunks
    ]

    print("Loading embedding model...")

    embedding_model = get_embedding_model()

    print("Creating ChromaDB...")

    vector_store = Chroma.from_documents(
        documents=langchain_documents,
        embedding=embedding_model,
        persist_directory=str(VECTOR_DB_PATH)
    )

    print(f"Vector database created at: {VECTOR_DB_PATH}")

    return vector_store


def get_vector_store():

    embedding_model = get_embedding_model()

    return Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embedding_model
    )
