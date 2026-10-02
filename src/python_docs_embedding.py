"""3단계: OpenAI Embedding 모델을 준비합니다."""

from langchain_openai import OpenAIEmbeddings

from python_docs_config import Settings, load_environment


def build_embeddings(settings: Settings) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=settings.embedding_model)


if __name__ == "__main__":
    load_environment()
    config = Settings()
    embeddings = build_embeddings(config)
    vector = embeddings.embed_query("언제 ValueError를 발생시켜야 하나요?")
    print("Embedding 모델:", config.embedding_model)
    print("벡터 길이:", len(vector))
    print("앞부분 10개 값:", vector[:10])
