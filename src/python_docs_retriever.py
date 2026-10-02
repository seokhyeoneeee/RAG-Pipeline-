"""6단계: Baseline Retriever와 Hybrid Retriever를 구성합니다."""

from __future__ import annotations

import re

from kiwipiepy import Kiwi
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

from python_docs_config import Settings, load_environment
from python_docs_loader import load_documents
from python_docs_splitter import split_documents
from python_docs_vectorstore import build_vectorstore


TOKEN_PATTERN = re.compile(r"[가-힣]+|[A-Za-z_][A-Za-z0-9_.]*|\d+")
IDENTIFIER_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*|\d+")
KIWI = Kiwi()


def regex_tokenize(text: str) -> list[str]:
    """형태소 분석 전 비교용 정규식 tokenizer입니다."""

    return TOKEN_PATTERN.findall(text.lower())


def kiwi_tokenize(text: str) -> list[str]:
    """Python 식별자와 한국어 내용 형태소를 추출합니다."""

    identifiers = IDENTIFIER_PATTERN.findall(text.lower())
    morphemes = [
        token.form.lower()
        for token in KIWI.tokenize(text)
        if token.tag.startswith(("NN", "VV", "VA", "XR"))
    ]
    return identifiers + morphemes


tokenize = kiwi_tokenize

def document_key(document: Document) -> tuple[str, int, str]:
    return (
        str(document.metadata.get("source", "")),
        int(document.metadata.get("start_index", -1)),
        document.page_content,
    )


class HybridRRFRetriever:
    """Dense와 BM25 순위를 weighted Reciprocal Rank Fusion으로 결합합니다."""

    def __init__(self, dense_retriever, bm25_retriever, settings: Settings):
        self.dense_retriever = dense_retriever
        self.bm25_retriever = bm25_retriever
        self.settings = settings

    def invoke(self, query: str) -> list[Document]:
        rankings = [
            (self.dense_retriever.invoke(query), self.settings.dense_weight),
            (self.bm25_retriever.invoke(query), self.settings.bm25_weight),
        ]
        scores: dict[tuple[str, int, str], float] = {}
        documents: dict[tuple[str, int, str], Document] = {}

        for ranking, weight in rankings:
            for rank, document in enumerate(ranking, start=1):
                key = document_key(document)
                documents[key] = document
                scores[key] = scores.get(key, 0.0) + weight / (
                    self.settings.rrf_constant + rank
                )

        ordered_keys = sorted(scores, key=scores.get, reverse=True)
        return [documents[key] for key in ordered_keys[: self.settings.hybrid_k]]


def build_retrievers(settings: Settings, rebuild: bool = False):
    chunks = split_documents(load_documents(), settings)
    vectorstore = build_vectorstore(chunks, settings, rebuild=rebuild)

    baseline = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.baseline_k},
    )
    dense_candidates = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.fetch_k},
    )
    regex_bm25 = BM25Retriever.from_documents(
        chunks, preprocess_func=regex_tokenize
    )
    regex_bm25.k = settings.fetch_k
    kiwi_bm25 = BM25Retriever.from_documents(
        chunks, preprocess_func=kiwi_tokenize
    )
    kiwi_bm25.k = settings.fetch_k

    hybrid_regex = HybridRRFRetriever(dense_candidates, regex_bm25, settings)
    hybrid_kiwi = HybridRRFRetriever(dense_candidates, kiwi_bm25, settings)
    return baseline, hybrid_regex, hybrid_kiwi


if __name__ == "__main__":
    load_environment()
    config = Settings()
    baseline_retriever, regex_retriever, kiwi_retriever = build_retrievers(config)
    question = "인코딩을 지정해 텍스트 파일을 읽는 pathlib 메서드는 무엇인가요?"

    for name, retriever in (
        ("Baseline", baseline_retriever),
        ("Hybrid Regex", regex_retriever),
        ("Hybrid Kiwi", kiwi_retriever),
    ):
        print(f"\n=== {name} ===")
        for rank, document in enumerate(retriever.invoke(question), start=1):
            print(rank, document.metadata["source"], document.metadata["start_index"])
