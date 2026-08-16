from langchain_core.prompts import ChatPromptTemplate

from app.rag.llm import get_llm
from app.rag.retriever import get_vector_store


PROMPT = """
You are DevOpsRAG, an intelligent DevOps troubleshooting assistant.

Answer the user's question using ONLY the provided context.

If the context does not contain enough information to answer
the question, clearly say that there is not enough information.

Do not invent logs, errors, configurations, or solutions.

Explain the answer in simple technical language.

Context:
{context}

User Question:
{question}

Answer:
"""


def ask_question(question: str):
    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    prompt = ChatPromptTemplate.from_template(PROMPT)

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    llm = get_llm()

    response = llm.invoke(messages)

    sources = [
        document.metadata.get("source")
        for document in results
    ]

    return {
        "question": question,
        "answer": response.content,
        "sources": sources
    }
