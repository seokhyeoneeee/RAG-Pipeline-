"""4단계: Embedding 벡터 사이의 Cosine Similarity를 확인합니다."""

import math

from python_docs_config import Settings, load_environment
from python_docs_embedding import build_embeddings


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    load_environment()
    embeddings = build_embeddings(Settings())
    sentences = [
        "언제 ValueError를 발생시켜야 하나요?",
        "인수의 타입은 맞지만 값이 잘못된 경우 어떤 예외를 사용하나요?",
        "pathlib으로 텍스트 파일을 어떻게 읽나요?",
    ]
    vectors = embeddings.embed_documents(sentences)
    print("문장 1 vs 문장 2:", cosine_similarity(vectors[0], vectors[1]))
    print("문장 1 vs 문장 3:", cosine_similarity(vectors[0], vectors[2]))
