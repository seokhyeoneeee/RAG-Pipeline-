"""1단계: Python 공식 문서 텍스트 파일을 Document로 로드합니다."""

from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

from python_docs_config import DATA_DIR


def load_documents(data_dir: Path = DATA_DIR) -> list[Document]:
    paths = sorted(data_dir.glob("*.txt"))
    if not paths:
        raise FileNotFoundError(f"No .txt documents found in {data_dir}")

    documents: list[Document] = []
    for path in paths:
        if path.name == "copyright.txt":
            continue

        loaded = TextLoader(str(path), encoding="utf-8").load()
        for document in loaded:
            document.metadata.update(
                {
                    "source": path.name,
                    "path": str(path),
                    "dataset": "Python 3.14 한국어 설명서",
                }
            )
        documents.extend(loaded)
    return documents


if __name__ == "__main__":
    docs = load_documents()
    print("문서 개수:", len(docs))
    print("첫 문서:", docs[0].metadata["source"])
    print(docs[0].page_content[:500])
