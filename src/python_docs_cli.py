"""Command-line entry point for querying and evaluating the project."""

from __future__ import annotations

import argparse

from python_docs_config import RESULT_PATH, Settings, load_environment
from python_docs_evaluation import (
    evaluate_generation,
    evaluate_retrievers,
    render_markdown,
    source_rows,
)
from python_docs_rag_pipeline import answer
from python_docs_retriever import build_retrievers


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Python documentation RAG")
    parser.add_argument(
        "--rebuild", action="store_true", help="rebuild the cached FAISS index"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    ask_parser = subparsers.add_parser("ask", help="answer one question")
    ask_parser.add_argument("question")
    subparsers.add_parser("evaluate", help="compare baseline and two hybrid retrievers")
    return parser.parse_args()


def main() -> None:
    load_environment()
    args = parse_args()
    settings = Settings()
    baseline, hybrid_regex, hybrid_kiwi = build_retrievers(
        settings, rebuild=args.rebuild
    )

    if args.command == "ask":
        response, documents = answer(args.question, hybrid_regex, settings)
        print(response)
        print("\n검색된 문서:")
        for row in source_rows(documents):
            print(f"{row['rank']}. {row['source']} (offset {row['start_index']})")
        return

    report = evaluate_retrievers(baseline, hybrid_regex, hybrid_kiwi)
    report["generation"] = evaluate_generation(
        baseline, hybrid_regex, settings
    )
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(render_markdown(report), encoding="utf-8")

    baseline_summary = report["summary"]["baseline"]
    regex_summary = report["summary"]["hybrid_regex"]
    kiwi_summary = report["summary"]["hybrid_kiwi"]
    print("=== Retrieval 평가 요약 ===")
    print(
        "Baseline - Hit Rate:",
        f"{baseline_summary['hit_rate']:.3f}",
        "MRR:",
        f"{baseline_summary['mrr']:.3f}",
    )
    print(
        "Hybrid Regex - Hit Rate:",
        f"{regex_summary['hit_rate']:.3f}",
        "MRR:",
        f"{regex_summary['mrr']:.3f}",
    )
    print(
        "Hybrid Kiwi  - Hit Rate:",
        f"{kiwi_summary['hit_rate']:.3f}",
        "MRR:",
        f"{kiwi_summary['mrr']:.3f}",
    )
    print("Generation 비교 질문:", len(report["generation"]))
    print(f"Markdown 결과: {RESULT_PATH}")


if __name__ == "__main__":
    main()
