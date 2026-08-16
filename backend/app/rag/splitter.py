from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for document in documents:
        split_texts = splitter.split_text(document["content"])

        for text in split_texts:
            chunks.append({
                "source": document["source"],
                "content": text
            })

    return chunks
