"""프로젝트 공통 경로, 모델명, 검색 설정."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "python_docs"
INDEX_DIR = PROJECT_ROOT / "data" / "index" / "python_docs_faiss"
INDEX_MANIFEST = INDEX_DIR.parent / "python_docs_manifest.json"
RESULT_PATH = PROJECT_ROOT / "results" / "python_docs_evaluation.md"


def load_environment() -> None:
    """프로젝트 루트의 .env를 읽고, 없으면 기존 src/.env를 사용합니다."""

    root_env = PROJECT_ROOT / ".env"
    fallback_env = PROJECT_ROOT / "src" / ".env"
    load_dotenv(root_env if root_env.exists() else fallback_env, override=True)


@dataclass(frozen=True)
class Settings:
    chunk_size: int = 900
    chunk_overlap: int = 150
    baseline_k: int = 4
    hybrid_k: int = 4
    fetch_k: int = 10
    dense_weight: float = 0.55
    bm25_weight: float = 0.45
    rrf_constant: int = 60
    embedding_model: str = field(
        default_factory=lambda: os.getenv(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        )
    )
    chat_model: str = field(
        default_factory=lambda: os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    )
