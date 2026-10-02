from __future__ import annotations

import sys
import os
import unittest
from pathlib import Path

from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from python_docs_config import PROJECT_ROOT, Settings  # noqa: E402
from python_docs_evaluation import render_markdown, retrieval_metrics  # noqa: E402
from python_docs_loader import load_documents  # noqa: E402
from python_docs_retriever import (  # noqa: E402
    HybridRRFRetriever,
    kiwi_tokenize,
    tokenize,
)
from python_docs_splitter import split_documents  # noqa: E402


class StaticRetriever:
    def __init__(self, documents):
        self.documents = documents

    def invoke(self, _query):
        return self.documents


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = Settings()
        cls.documents = load_documents()
        cls.chunks = split_documents(cls.documents, cls.settings)

    def test_dataset_and_chunking(self):
        self.assertEqual(len(self.documents), 24)
        self.assertGreater(len(self.chunks), len(self.documents))
        self.assertTrue(all("source" in chunk.metadata for chunk in self.chunks))

    def test_dataset_path_does_not_depend_on_working_directory(self):
        original = Path.cwd()
        try:
            os.chdir(PROJECT_ROOT / "src")
            self.assertEqual(len(load_documents()), 24)
        finally:
            os.chdir(original)

    def test_tokenizer_keeps_python_identifier(self):
        tokens = tokenize("pathlib.Path.read_text로 텍스트 파일을 읽습니다")
        self.assertIn("pathlib.path.read_text", tokens)
        self.assertIn("텍스트", tokens)

    def test_kiwi_removes_korean_particles(self):
        tokens = kiwi_tokenize("예외를 처리하고 값을 반환합니다")
        self.assertIn("예외", tokens)
        self.assertIn("처리", tokens)
        self.assertIn("값", tokens)

    def test_bm25_finds_pathlib(self):
        retriever = BM25Retriever.from_documents(
            self.chunks, preprocess_func=tokenize
        )
        retriever.k = 4
        results = retriever.invoke("pathlib Path read_text encoding")
        self.assertEqual(results[0].metadata["source"], "pathlib.txt")

    def test_rrf_rewards_agreement(self):
        a = Document(
            page_content="a", metadata={"source": "a.txt", "start_index": 0}
        )
        b = Document(
            page_content="b", metadata={"source": "b.txt", "start_index": 0}
        )
        c = Document(
            page_content="c", metadata={"source": "c.txt", "start_index": 0}
        )
        retriever = HybridRRFRetriever(
            StaticRetriever([a, b]), StaticRetriever([b, c]), self.settings
        )
        results = retriever.invoke("unused")
        self.assertEqual(results[0].metadata["source"], "b.txt")

    def test_retrieval_metrics(self):
        documents = [
            Document(page_content="a", metadata={"source": "a.txt"}),
            Document(page_content="b", metadata={"source": "b.txt"}),
        ]
        metrics = retrieval_metrics(documents, ["b.txt"])
        self.assertEqual(metrics["hit"], 1)
        self.assertEqual(metrics["first_relevant_rank"], 2)
        self.assertEqual(metrics["reciprocal_rank"], 0.5)

    def test_markdown_report(self):
        report = {
            "summary": {
                "baseline": {"hit_rate": 1.0, "mrr": 0.5, "scored_questions": 1},
                "hybrid_regex": {
                    "hit_rate": 1.0,
                    "mrr": 0.5,
                    "scored_questions": 1,
                },
                "hybrid_kiwi": {
                    "hit_rate": 1.0,
                    "mrr": 1.0,
                    "scored_questions": 1,
                },
            },
            "results": [
                {
                    "id": "sample",
                    "question": "테스트 질문",
                    "baseline": {
                        "hit": 0,
                        "first_relevant_rank": None,
                        "reciprocal_rank": 0.0,
                        "documents": [],
                    },
                    "hybrid_regex": {
                        "hit": 0,
                        "first_relevant_rank": None,
                        "reciprocal_rank": 0.0,
                        "documents": [],
                    },
                    "hybrid_kiwi": {
                        "hit": 1,
                        "first_relevant_rank": 1,
                        "reciprocal_rank": 1.0,
                        "documents": [],
                    },
                }
            ],
            "generation": [
                {
                    "number": 1,
                    "question": "테스트 질문",
                    "baseline": {
                        "answer": "기준 답변 [a.txt]",
                        "grounded": True,
                        "search_result": "Hit · 정답 1위",
                        "documents": [
                            {
                                "rank": 1,
                                "source": "a.txt",
                                "start_index": 0,
                                "preview": "a",
                            }
                        ],
                    },
                    "improved": {
                        "answer": "개선 답변 [a.txt]",
                        "grounded": True,
                        "search_result": "Hit · 정답 1위",
                        "documents": [
                            {
                                "rank": 1,
                                "source": "a.txt",
                                "start_index": 0,
                                "preview": "a",
                            }
                        ],
                    },
                    "change": "동일",
                    "judgment": "두 답변 모두 기대 내용과 출처를 충족",
                }
            ],
        }
        markdown = render_markdown(report)
        self.assertIn("# Python 공식 문서 RAG 평가 결과", markdown)
        self.assertIn("| MRR@4 | 0.500 | 0.500 | 1.000 |", markdown)
        self.assertIn("테스트 질문", markdown)
        self.assertIn("| Baseline | 0 | Top-4 내 없음 | 0.000 |", markdown)
        self.assertIn("## 2. 대표 질문 Generation 비교", markdown)
        self.assertIn("기준 답변 [a.txt]", markdown)
        self.assertIn("Hit · 정답 1위", markdown)
        self.assertIn("### 지표 그래프", markdown)


if __name__ == "__main__":
    unittest.main()
