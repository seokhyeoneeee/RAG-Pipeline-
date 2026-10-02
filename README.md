# Python 공식 문서 기반 오류·개념 Q&A RAG

## 프로젝트 한눈에 보기

| 항목 | 내용 |
|---|---|
| 한 문장 정의 | Python 3.14 공식 문서를 근거로 입문자의 오류·문법·표준 라이브러리 질문에 답하는 RAG |
| 대상 사용자 | Python 입문자, 주니어 개발자, 공식 문서 학습자 |
| 데이터 | 공식 한국어 문서 25개 파일 중 라이선스를 제외한 24개 검색 |
| Baseline | OpenAI Embedding + FAISS Similarity Search Top-4 |
| 기본 개선안 | Dense Search + 정규식 BM25 + weighted RRF Top-4 |
| 평가셋 | 한국어 질문 25개: Retrieval 24개, 문서 밖 질문 1개 |
| 최종 결과 | Hit Rate@4 0.875 유지, MRR@4 0.674 → 0.781 |
| 근거 없음 처리 | `제공된 Python 공식 문서에서 확인할 수 없습니다.`라고 답변 |

### 핵심 산출물

| 문서 | 용도 |
|---|---|
| [`README.md`](README.md) | 설치·실행·구조·전체 결과 안내 |
| [`results/python_docs_design.md`](results/python_docs_design.md) | 데이터 범위와 RAG 설계 |
| [`results/python_docs_evaluation.md`](results/python_docs_evaluation.md) | Retrieval·Generation 상세 평가 |

`data/`는 제출 대상에서 제외할 수 있습니다. 사용한 데이터의 출처, 범위, 제외 항목과 전처리 내역은 설계 문서에 기록했습니다.

## 1. 문제 정의

Python 입문자는 오류 메시지, 문법, 표준 라이브러리를 학습할 때 공식 문서의 여러 페이지를 직접 찾아야 합니다. 또한 질문에는 `ValueError`, `dict.get`, `Path.read_text` 같은 정확한 식별자와 "예외가 발생해도 정리 코드를 실행하려면?" 같은 자연어 표현이 함께 사용됩니다.

이 프로젝트는 Python 3.14 공식 문서만 검색하여 다음 원칙으로 답합니다.

- 검색된 공식 문서만 답변 근거로 사용합니다.
- 답변에 근거 파일명을 표시합니다.
- 문서에서 확인할 수 없는 내용은 추측하지 않고 답변을 거절합니다.
- 같은 질문셋으로 Baseline과 개선 검색의 성능을 비교합니다.

주요 대상은 Python 입문자, 주니어 개발자, 공식 문서를 학습하는 사용자입니다.

## 2. 사용 데이터

- 출처: [Python 3.14 공식 한국어 문서 일반 텍스트 아카이브](https://docs.python.org/ko/3/download.html)
- 경로: `data/python_docs/*.txt`
- 규모: 텍스트 파일 25개, 약 845 KiB
- 검색 대상: 라이선스 문서를 제외한 24개 문서
- 라이선스: Python Software Foundation License Version 2

데이터 범위는 Python Tutorial 전체, built-in types/functions/exceptions, `pathlib`, `dataclasses`, `venv`, Programming FAQ입니다. `docs.python.org/ko`에서 배포하는 공식 한국어 아카이브의 파일을 그대로 사용하며, 별도 기계번역 단계는 없습니다.

## 3. RAG 구조

### Baseline

```text
TextLoader -> RecursiveCharacterTextSplitter -> OpenAI Embeddings
           -> FAISS -> Similarity Search Top-4 -> Prompt -> ChatOpenAI -> Answer
```

### 개선 Pipeline

```text
                              -> Dense Search Top-10 --\
Question -> Query ------------------------------------> Weighted RRF -> Top-4
                              -> BM25 Search Top-10 ---/
                                                       -> Prompt -> LLM -> Answer
```

- Chunk size: 900자
- Chunk overlap: 150자
- Embedding: `text-embedding-3-small`
- Vector Store: FAISS
- Baseline: Dense similarity Top-4
- 개선안: Dense 0.55 + BM25 0.45 weighted Reciprocal Rank Fusion
- BM25 토큰화: 정규식 방식과 Kiwi 형태소 방식

코드는 기존 단계별 실습 형식에 맞춰 분리했습니다.

| 단계 | 파일 | 역할 |
|---|---|---|
| 공통 설정 | `python_docs_config.py` | 경로, 모델명, 검색 설정, 환경변수 |
| Loader | `python_docs_loader.py` | 텍스트 문서 로드 및 metadata 추가 |
| Splitter | `python_docs_splitter.py` | 문서를 검색용 Chunk로 분할 |
| Embedding | `python_docs_embedding.py` | OpenAI Embedding 모델 생성 |
| Similarity | `python_docs_similarity.py` | Cosine Similarity 확인 |
| Vector Store | `python_docs_vectorstore.py` | FAISS 생성, 저장, 재사용 |
| Retriever | `python_docs_retriever.py` | Baseline, 정규식 Hybrid, Kiwi Hybrid 구성 |
| Prompt·LLM | `python_docs_prompt_llm.py` | 근거 제한 Prompt와 LLM 구성 |
| RAG Pipeline | `python_docs_rag_pipeline.py` | 검색부터 답변 생성까지 연결 |
| Evaluation | `python_docs_evaluation.py` | 고정 질문셋, 정답 source, Hit Rate와 MRR 계산 |
| CLI | `python_docs_cli.py` | 질문 및 평가 명령 실행 |

## 4. 설치 방법

요구 Python 버전은 `>=3.11,<3.12`이며 `uv sync`가 이 조건에 맞는 환경을 구성합니다.

```bash
git clone https://github.com/seokhyeoneeee/RAG-Pipeline-.git
cd RAG-Pipeline-
uv sync
cp .env.example .env
```

`.env`에 유효한 OpenAI API key를 입력합니다.

```env
OPENAI_API_KEY=replace-with-your-key
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## 5. 실행 방법

질문 하나에 답하기:

```bash
uv run python src/python_docs_cli.py ask \
  "변경 가능한 기본 인수가 함수 호출 사이에서 공유되는 이유는 무엇인가요?"
```

Baseline과 두 Hybrid Retriever 평가하기:

```bash
uv run python src/python_docs_cli.py evaluate
```

문서나 Chunk 설정을 바꾼 후 FAISS index를 다시 만들기:

```bash
uv run python src/python_docs_cli.py --rebuild evaluate
```

각 단계를 개별적으로 확인할 수도 있습니다.

```bash
uv run python src/python_docs_loader.py
uv run python src/python_docs_splitter.py
uv run python src/python_docs_embedding.py
uv run python src/python_docs_similarity.py
uv run python src/python_docs_vectorstore.py
uv run python src/python_docs_retriever.py
uv run python src/python_docs_prompt_llm.py
uv run python src/python_docs_rag_pipeline.py
```

평가 상세 결과는 질문별 검색 순위와 대표 질문의 실제 Baseline·Regex Hybrid 답변 비교를 포함해 `results/python_docs_evaluation.md`에 저장됩니다.

## 6. 테스트 질문

Baseline과 두 개선 Pipeline에 아래 25개 질문을 동일하게 사용합니다. 정답 문서가 있는 24개 질문은 검색 평가에 사용하고, 마지막 질문은 문서에 근거가 없을 때 답변을 거절하는지 확인합니다.

| 유형 | 질문 | 정답 문서 |
|---|---|---|
| 정확한 예외명 | 인수의 타입은 올바르지만 값이 부적절할 때는 왜 TypeError가 아니라 ValueError를 발생시켜야 하나요? | `exceptions.txt` |
| 바꿔 말한 질문 | 예외 발생 여부와 관계없이 반드시 실행해야 하는 정리 코드는 어디에 작성해야 하나요? | `errors.txt` |
| 개념 질문 | 전체 반복문을 작성하지 않고 표현식과 for 절로 리스트를 만드는 방법은 무엇인가요? | `datastructures.txt` |
| 정확한 메서드명 | 키가 없고 기본값도 지정하지 않았을 때 dict.get은 무엇을 반환하나요? | `stdtypes.txt` |
| 정확한 API명 | 인코딩을 지정하여 텍스트 파일을 읽을 수 있는 pathlib 메서드는 무엇인가요? | `pathlib.txt` |
| 설정 질문 | 데이터클래스에 frozen=True를 지정하면 객체가 완전히 불변이 되나요? | `dataclasses.txt` |
| 바꿔 말한 질문 | 가상환경의 Python 인터프리터를 사용하려면 반드시 가상환경을 활성화해야 하나요? | `library_venv.txt` 또는 `tutorial_venv.txt` |
| FAQ | 변경 가능한 기본 인수가 여러 함수 호출 사이에서 공유되는 이유는 무엇인가요? | `programming.txt` |
| 복합 질문 | 스크립트를 직접 실행할 때 __name__의 값은 무엇이며, 이를 이용해 직접 실행할 때만 코드를 실행하려면 어떻게 하나요? | `modules.txt` |
| 범위 함수 | range 함수가 만드는 수열에 stop 값 자체도 포함되나요? | `stdtypes.txt` |
| 리스트 메서드 | 리스트의 append와 extend는 어떤 차이가 있나요? | `datastructures.txt` |
| 튜플 문법 | 요소가 하나뿐인 튜플을 만들 때 끝에 쉼표가 필요한 이유는 무엇인가요? | `datastructures.txt` |
| 집합 생성 | 빈 집합을 만들 때 중괄호 대신 set 함수를 사용해야 하는 이유는 무엇인가요? | `datastructures.txt` |
| 파일 인코딩 | open 함수에서 encoding을 생략하면 어떤 인코딩이 사용되나요? | `functions.txt` 또는 `inputoutput.txt` |
| 자원 정리 | 파일을 with 문으로 열면 작업이 끝난 뒤 자동으로 닫히나요? | `inputoutput.txt` |
| 모듈 검색 | import할 모듈을 찾을 때 Python은 어떤 경로들을 검색하나요? | `modules.txt` |
| 이름 규칙 | 클래스에서 밑줄로 시작하는 이름은 비공개 멤버를 뜻하나요? | `classes.txt` |
| 제너레이터 | 제너레이터 함수에서 yield는 어떤 역할을 하나요? | `classes.txt` |
| 부동소수점 | 0.1 같은 십진 소수를 Python이 정확히 표현하지 못할 수 있는 이유는 무엇인가요? | `floatingpoint.txt` |
| 가상환경 생성 | venv 모듈로 새로운 가상환경을 만드는 기본 명령은 무엇인가요? | `library_venv.txt` 또는 `tutorial_venv.txt` |
| 데이터클래스 옵션 | 데이터클래스에서 order=True를 쓰면서 eq=False를 지정하면 어떻게 되나요? | `dataclasses.txt` |
| 경로 확인 | pathlib Path가 가리키는 파일이나 디렉터리가 실제로 존재하는지 어떻게 확인하나요? | `pathlib.txt` |
| 예외 처리 | try 문의 else 절은 언제 실행되나요? | `errors.txt` |
| 반복 인덱스 | 반복 가능한 객체의 항목과 인덱스를 함께 얻으려면 어떤 함수를 사용하나요? | `functions.txt` 또는 `datastructures.txt` |
| 문서에 없는 질문 | pathlib.Path 객체를 Amazon S3 버킷에 직접 업로드하려면 어떻게 하나요? | 평가 제외·답변 거절 확인 |

평가 기준은 정답 source가 Top-4에 포함되는지를 보는 Hit Rate@4와 첫 정답 source 순위의 reciprocal rank 평균인 MRR@4입니다. 문서에 없는 질문은 Retrieval 점수에서 제외합니다.

## 7. Baseline 결과

한국어 문서와 한국어 질문으로 정답 문서가 있는 24개 질문을 평가한 결과입니다.

| 지표 | Baseline |
|---|---:|
| Hit Rate@4 | 0.875 |
| MRR@4 | 0.674 |
| 평가 질문 수 | 24 |

Baseline은 24개 중 21개의 정답 문서를 Top-4에서 찾았습니다. Q1, Q9, Q11은 정답 문서가 Top-4에 없어 miss로 판정되었습니다.

## 8. 개선 방법과 결과

개선 방법은 Dense Search와 BM25를 결합한 Hybrid Search입니다. Dense Search는 자연어 의미와 바꿔 말한 표현에 강하고, BM25는 `ValueError`, `dict.get`, `Path.read_text` 같은 정확한 토큰에 강합니다. Weighted RRF가 두 검색 결과의 순위를 하나로 합칩니다.

`kiwipiepy`의 Kiwi 형태소 토큰화는 영문 식별자를 별도로 보존하고 명사·동사·형용사·어근을 BM25 토큰으로 사용합니다.

| 지표 | Baseline | Hybrid Regex | Hybrid Kiwi |
|---|---:|---:|---:|
| Hit Rate@4 | 0.875 | 0.875 | 0.875 |
| MRR@4 | 0.674 | 0.781 | 0.747 |
| 평가 질문 수 | 24 | 24 | 24 |

두 Hybrid 방식 모두 Hit Rate는 Baseline과 같았지만 정답 문서의 순위를 높였습니다. 정규식 Hybrid의 MRR은 0.781, Kiwi Hybrid의 MRR은 0.747입니다. 두 점수 차이가 작으므로 더 단순하고 형태소 분석 단계가 필요 없는 정규식 Hybrid를 기본 질문 응답에 사용합니다. Kiwi Hybrid는 동일 질문셋의 비교 결과로 유지합니다.

### 생성 답변 확인

`gpt-4o-mini`, temperature 0으로 Baseline과 기본 Regex Hybrid의 답변을 직접 확인했습니다.

| 질문 | Baseline | Regex Hybrid | 확인 결과 |
|---|---|---|---|
| Q2 `finally` | `finally` 절과 `errors.txt` 제시 | 같은 답과 출처 제시 | 둘 다 근거와 일치 |
| Q3 리스트 컴프리헨션 | 개념·문법과 `datastructures.txt` 제시 | 예제와 같은 출처 제시 | 둘 다 근거와 일치 |
| Q6 `frozen=True` | 확인 불가로 답변 | 확인 불가로 답변 | 둘 다 기대 내용이 포함된 청크를 확보하지 못해 실패 |
| Q8 변경 가능한 기본 인수 | 정의 시 한 번 생성된다는 답과 `programming.txt` 제시 | 같은 답과 출처 제시 | 둘 다 근거와 일치 |
| Q25 S3 업로드 | “제공된 Python 공식 문서에서 확인할 수 없습니다.” | 같은 거절 문구 | 둘 다 문서 밖 정보를 추측하지 않음 |

Retrieval 점수가 높아도 정답 파일 안의 적절한 설명이 Prompt에 전달되지 않으면 Q6처럼 생성 답변이 실패할 수 있습니다. 따라서 Retrieval 지표와 생성 답변 확인을 함께 사용합니다.

## 9. 한계와 추가 개선 방향

- Q1의 정답 부분은 `exceptions.txt`에 “Raised when an operation or function receives an argument that has the right type but an inappropriate value.”라고 영어로 남아 있습니다. 한국어 질문과의 의미 연결이 약해 Top-4에서 누락됐습니다. Query Rewrite로 `right type`, `inappropriate value`, `ValueError` 같은 영어 표현을 보강할 수 있습니다.
- Q9의 정답 `modules.txt` 청크는 정규식 BM25 단독 검색에서 3위였지만 Dense 검색에서는 Top-10 밖이었습니다. RRF에서 두 검색에 함께 등장한 청크와 Dense 상위 청크의 합산 점수가 더 높아 최종 Top-4에서 밀렸습니다. Reranker를 추가하거나 BM25 가중치를 높여 보완할 수 있습니다.
- 공식 한국어 번역본에도 아직 영어로 남은 일부 문단이 있습니다. 번역이 갱신되면 데이터와 FAISS index를 다시 생성해야 합니다.
- 현재 정답은 파일 단위로 지정되어 같은 파일의 무관한 Chunk도 hit로 판정될 수 있습니다. Chunk ID 단위 relevance label이 더 정확합니다.
- 평가 질문을 25개로 늘렸지만 Retrieval 점수에 포함되는 질문은 24개입니다. 질문 하나가 1위에서 2위로 내려가면 MRR이 약 0.021 변하므로, 더 안정적인 비교에는 30~50개 이상의 평가셋이 필요합니다.
- Hybrid 가중치 0.55/0.45와 Chunk 크기 900은 평가 전에 사전 지정한 값이며, 현재 평가셋 결과를 보고 조정하지 않았습니다. 별도의 검증 질문셋을 두고 조정해야 과적합을 줄일 수 있습니다.
- Kiwi의 품사 선택, 사용자 사전, BM25 가중치를 조정하면 검색 순위를 더 개선할 수 있습니다.
- 생성 답변은 대표 질문을 수동 확인했으며 아직 자동 점수화하지 않습니다. Faithfulness, answer relevance, citation correctness 평가를 추가할 수 있습니다.
- OpenAI API에 의존하므로 비용, network, API key 상태에 영향을 받습니다. 로컬 Embedding과 로컬 LLM을 대안으로 비교할 수 있습니다.
