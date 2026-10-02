"""2단계: 로드한 문서를 검색 가능한 Chunk로 분할합니다."""

from collections.abc import Iterable

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from python_docs_config import Settings
from python_docs_loader import load_documents


def split_documents(
    documents: Iterable[Document], settings: Settings
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(list(documents))


if __name__ == "__main__":
    config = Settings()
    docs = load_documents()
    chunks = split_documents(docs, config)
    print("원본 Document 수:", len(docs))
    print("Chunk 수:", len(chunks))
    print("첫 Chunk metadata:", chunks[0].metadata)
    print(chunks[0].page_content[:500])
