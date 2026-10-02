"""5단계: Chunk를 Embedding하여 FAISS Vector Store를 생성·저장합니다."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from python_docs_config import (
    DATA_DIR,
    INDEX_DIR,
    INDEX_MANIFEST,
    Settings,
    load_environment,
)
from python_docs_embedding import build_embeddings
from python_docs_loader import load_documents
from python_docs_splitter import split_documents


def dataset_fingerprint(data_dir: Path, settings: Settings) -> str:
    digest = hashlib.sha256()
    digest.update(
        f"{settings.chunk_size}:{settings.chunk_overlap}:"
        f"{settings.embedding_model}".encode()
    )
    for path in sorted(data_dir.glob("*.txt")):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def build_vectorstore(
    chunks: list[Document], settings: Settings, rebuild: bool = False
) -> FAISS:
    embeddings = build_embeddings(settings)
    fingerprint = dataset_fingerprint(DATA_DIR, settings)

    if not rebuild and INDEX_DIR.exists() and INDEX_MANIFEST.exists():
        manifest = json.loads(INDEX_MANIFEST.read_text(encoding="utf-8"))
        if manifest.get("fingerprint") == fingerprint:
            return FAISS.load_local(
                str(INDEX_DIR),
                embeddings,
                allow_dangerous_deserialization=True,
            )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))
    INDEX_MANIFEST.write_text(
        json.dumps(
            {
                "fingerprint": fingerprint,
                "embedding_model": settings.embedding_model,
                "chunk_count": len(chunks),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return vectorstore


if __name__ == "__main__":
    load_environment()
    config = Settings()
    chunks = split_documents(load_documents(), config)
    store = build_vectorstore(chunks, config)
    results = store.similarity_search("언제 ValueError를 발생시켜야 하나요?", k=3)
    for rank, document in enumerate(results, start=1):
        print(f"\n[{rank}] {document.metadata['source']}")
        print(document.page_content[:500])
