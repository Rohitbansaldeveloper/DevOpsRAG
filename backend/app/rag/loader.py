from pathlib import Path


def load_documents(directory: str):
    documents = []

    directory_path = Path(directory)

    if not directory_path.exists():
        raise FileNotFoundError(
            f"Knowledge directory does not exist: {directory_path.resolve()}"
        )

    for file_path in directory_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [".txt", ".md"]:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read().strip()

            if text:
                documents.append({
                    "source": str(file_path),
                    "content": text
                })

    return documents
