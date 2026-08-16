import os

from langchain_ollama import OllamaEmbeddings


def get_embedding_model():

    ollama_url = os.getenv(
        "OLLAMA_BASE_URL",
        "http://host.docker.internal:11434"
    )

    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=ollama_url
    )
