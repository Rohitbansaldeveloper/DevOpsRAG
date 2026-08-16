import os

from langchain_ollama import ChatOllama


def get_llm():
    return ChatOllama(
        model=os.getenv("LLM_MODEL", "llama3.2"),
        temperature=0,
        base_url=os.getenv(
            "OLLAMA_BASE_URL",
            "http://host.docker.internal:11434"
        )
    )
