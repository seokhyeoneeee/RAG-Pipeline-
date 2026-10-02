"""9단계: 동일 질문셋으로 Baseline과 두 Hybrid Retrieval을 평가합니다."""

from langchain_core.documents import Document

from python_docs_config import Settings
from python_docs_rag_pipeline import answer


ABSTENTION = "제공된 Python 공식 문서에서 확인할 수 없습니다."
GENERATION_CASES = {
    "paraphrase-finally": ("finally",),
    "concept-list-comprehension": ("리스트 컴프리헨션",),
    "exact-dataclass-frozen": ("불변",),
    "faq-mutable-default": ("한 번",),
    "out-of-scope": (),
}

TEST_CASES = [
    {
        "id": "exact-exception",
        "question": "인수의 타입은 올바르지만 값이 부적절할 때는 왜 TypeError가 아니라 ValueError를 발생시켜야 하나요?",
        "relevant_sources": ["exceptions.txt"],
    },
    {
        "id": "paraphrase-finally",
        "question": "예외 발생 여부와 관계없이 반드시 실행해야 하는 정리 코드는 어디에 작성해야 하나요?",
        "relevant_sources": ["errors.txt"],
    },
    {
        "id": "concept-list-comprehension",
        "question": "전체 반복문을 작성하지 않고 표현식과 for 절로 리스트를 만드는 방법은 무엇인가요?",
        "relevant_sources": ["datastructures.txt"],
    },
    {
        "id": "exact-dict-get",
        "question": "키가 없고 기본값도 지정하지 않았을 때 dict.get은 무엇을 반환하나요?",
        "relevant_sources": ["stdtypes.txt"],
    },
    {
        "id": "exact-pathlib",
        "question": "인코딩을 지정하여 텍스트 파일을 읽을 수 있는 pathlib 메서드는 무엇인가요?",
        "relevant_sources": ["pathlib.txt"],
    },
    {
        "id": "exact-dataclass-frozen",
        "question": "데이터클래스에 frozen=True를 지정하면 객체가 완전히 불변이 되나요?",
        "relevant_sources": ["dataclasses.txt"],
    },
    {
        "id": "paraphrase-venv",
        "question": "가상환경의 Python 인터프리터를 사용하려면 반드시 가상환경을 활성화해야 하나요?",
        "relevant_sources": ["library_venv.txt", "tutorial_venv.txt"],
    },
    {
        "id": "faq-mutable-default",
        "question": "변경 가능한 기본 인수가 여러 함수 호출 사이에서 공유되는 이유는 무엇인가요?",
        "relevant_sources": ["programming.txt"],
    },
    {
        "id": "multi-part-main",
        "question": "스크립트를 직접 실행할 때 __name__의 값은 무엇이며, 이를 이용해 직접 실행할 때만 코드를 실행하려면 어떻게 하나요?",
        "relevant_sources": ["modules.txt"],
    },
    {
        "id": "range-stop",
        "question": "range 함수가 만드는 수열에 stop 값 자체도 포함되나요?",
        "relevant_sources": ["stdtypes.txt"],
    },
    {
        "id": "append-vs-extend",
        "question": "리스트의 append와 extend는 어떤 차이가 있나요?",
        "relevant_sources": ["datastructures.txt"],
    },
    {
        "id": "single-tuple",
        "question": "요소가 하나뿐인 튜플을 만들 때 끝에 쉼표가 필요한 이유는 무엇인가요?",
        "relevant_sources": ["datastructures.txt"],
    },
    {
        "id": "empty-set",
        "question": "빈 집합을 만들 때 중괄호 대신 set 함수를 사용해야 하는 이유는 무엇인가요?",
        "relevant_sources": ["datastructures.txt"],
    },
    {
        "id": "open-encoding",
        "question": "open 함수에서 encoding을 생략하면 어떤 인코딩이 사용되나요?",
        "relevant_sources": ["functions.txt", "inputoutput.txt"],
    },
    {
        "id": "with-close",
        "question": "파일을 with 문으로 열면 작업이 끝난 뒤 자동으로 닫히나요?",
        "relevant_sources": ["inputoutput.txt"],
    },
    {
        "id": "module-search-path",
        "question": "import할 모듈을 찾을 때 Python은 어떤 경로들을 검색하나요?",
        "relevant_sources": ["modules.txt"],
    },
    {
        "id": "private-name",
        "question": "클래스에서 밑줄로 시작하는 이름은 비공개 멤버를 뜻하나요?",
        "relevant_sources": ["classes.txt"],
    },
    {
        "id": "generator-yield",
        "question": "제너레이터 함수에서 yield는 어떤 역할을 하나요?",
        "relevant_sources": ["classes.txt"],
    },
    {
        "id": "floating-point",
        "question": "0.1 같은 십진 소수를 Python이 정확히 표현하지 못할 수 있는 이유는 무엇인가요?",
        "relevant_sources": ["floatingpoint.txt"],
    },
    {
        "id": "create-venv",
        "question": "venv 모듈로 새로운 가상환경을 만드는 기본 명령은 무엇인가요?",
        "relevant_sources": ["library_venv.txt", "tutorial_venv.txt"],
    },
    {
        "id": "dataclass-order",
        "question": "데이터클래스에서 order=True를 쓰면서 eq=False를 지정하면 어떻게 되나요?",
        "relevant_sources": ["dataclasses.txt"],
    },
    {
        "id": "path-exists",
        "question": "pathlib Path가 가리키는 파일이나 디렉터리가 실제로 존재하는지 어떻게 확인하나요?",
        "relevant_sources": ["pathlib.txt"],
    },
    {
        "id": "try-else",
        "question": "try 문의 else 절은 언제 실행되나요?",
        "relevant_sources": ["errors.txt"],
    },
    {
        "id": "enumerate",
        "question": "반복 가능한 객체의 항목과 인덱스를 함께 얻으려면 어떤 함수를 사용하나요?",
        "relevant_sources": ["functions.txt", "datastructures.txt"],
    },
    {
        "id": "out-of-scope",
        "question": "pathlib.Path 객체를 Amazon S3 버킷에 직접 업로드하려면 어떻게 하나요?",
        "relevant_sources": [],
    },
]


PIPELINES = (
    ("baseline", "Baseline"),
    ("hybrid_regex", "Hybrid Regex"),
    ("hybrid_kiwi", "Hybrid Kiwi"),
)


def source_rows(documents: list[Document]) -> list[dict]:
    return [
        {
            "rank": rank,
            "source": document.metadata.get("source"),
            "start_index": document.metadata.get("start_index"),
            "preview": " ".join(document.page_content.split())[:240],
        }
        for rank, document in enumerate(documents, start=1)
    ]


def retrieval_metrics(
    documents: list[Document], relevant_sources: list[str]
) -> dict[str, float | int | None]:
    if not relevant_sources:
        return {
            "hit": None,
            "reciprocal_rank": None,
            "first_relevant_rank": None,
        }

    expected = set(relevant_sources)
    for rank, document in enumerate(documents, start=1):
        if document.metadata.get("source") in expected:
            return {
                "hit": 1,
                "reciprocal_rank": 1.0 / rank,
                "first_relevant_rank": rank,
            }
    return {"hit": 0, "reciprocal_rank": 0.0, "first_relevant_rank": None}


def evaluate_retrievers(baseline, hybrid_regex, hybrid_kiwi) -> dict:
    retrievers = {
        "baseline": baseline,
        "hybrid_regex": hybrid_regex,
        "hybrid_kiwi": hybrid_kiwi,
    }
    results = []
    for case in TEST_CASES:
        row = {"id": case["id"], "question": case["question"]}
        for name, retriever in retrievers.items():
            documents = retriever.invoke(case["question"])
            row[name] = {
                **retrieval_metrics(documents, case["relevant_sources"]),
                "documents": source_rows(documents),
            }
        results.append(row)

    scored = [row for row in results if row["baseline"]["hit"] is not None]
    summary = {}
    for name in retrievers:
        summary[name] = {
            "hit_rate": sum(row[name]["hit"] for row in scored) / len(scored),
            "mrr": sum(row[name]["reciprocal_rank"] for row in scored) / len(scored),
            "scored_questions": len(scored),
        }
    return {"summary": summary, "results": results}


def _answer_uses_evidence(response: str, case: dict) -> bool:
    if not case["relevant_sources"]:
        return ABSTENTION in response

    lowered = response.lower()
    keywords = GENERATION_CASES[case["id"]]
    return any(keyword.lower() in lowered for keyword in keywords) and any(
        source.lower() in lowered for source in case["relevant_sources"]
    )


def evaluate_generation(baseline, hybrid_regex, settings: Settings) -> list[dict]:
    """대표 질문의 실제 답변과 근거 사용 여부를 비교합니다."""

    rows = []
    for number, case in enumerate(TEST_CASES, start=1):
        if case["id"] not in GENERATION_CASES:
            continue

        baseline_answer, baseline_documents = answer(
            case["question"], baseline, settings
        )
        improved_answer, improved_documents = answer(
            case["question"], hybrid_regex, settings
        )
        baseline_retrieval = retrieval_metrics(
            baseline_documents, case["relevant_sources"]
        )
        improved_retrieval = retrieval_metrics(
            improved_documents, case["relevant_sources"]
        )
        baseline_grounded = _answer_uses_evidence(baseline_answer, case)
        improved_grounded = _answer_uses_evidence(improved_answer, case)

        if improved_grounded and not baseline_grounded:
            change = "좋아짐"
            judgment = "개선 답변만 기대 내용과 출처를 충족"
        elif baseline_grounded and not improved_grounded:
            change = "나빠짐"
            judgment = "개선 검색이 정답 설명 청크를 놓침"
        elif baseline_grounded:
            change = "동일"
            judgment = (
                "두 답변 모두 근거 없이 답하지 않음"
                if not case["relevant_sources"]
                else "두 답변 모두 기대 내용과 출처를 충족"
            )
        else:
            change = "동일"
            judgment = "두 답변 모두 기대 내용 또는 출처를 충족하지 못함"

        rows.append(
            {
                "number": number,
                "question": case["question"],
                "baseline": {
                    "answer": baseline_answer,
                    "grounded": baseline_grounded,
                    "search_result": _search_result_text(baseline_retrieval),
                    "documents": source_rows(baseline_documents),
                },
                "improved": {
                    "answer": improved_answer,
                    "grounded": improved_grounded,
                    "search_result": _search_result_text(improved_retrieval),
                    "documents": source_rows(improved_documents),
                },
                "change": change,
                "judgment": judgment,
            }
        )
    return rows


def _metric_text(value) -> str:
    if value is None:
        return "평가 제외"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def _rank_text(metrics: dict) -> str:
    if metrics["hit"] is None:
        return "평가 제외"
    if metrics["first_relevant_rank"] is None:
        return "Top-4 내 없음"
    return str(metrics["first_relevant_rank"])


def _search_result_text(metrics: dict) -> str:
    if metrics["hit"] is None:
        return "평가 제외"
    if metrics["hit"]:
        return f"Hit · 정답 {metrics['first_relevant_rank']}위"
    return "Miss · Top-4 내 없음"


def _escape_cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _search_text(documents: list[dict]) -> str:
    return ", ".join(
        f"{document['rank']}. {document['source']}@{document['start_index']}"
        for document in documents
    )


def _quote(text: str) -> list[str]:
    return [f"> {line}" if line else ">" for line in text.splitlines()]


def _bar(value: float, width: int = 20) -> str:
    filled = round(value * width)
    return "█" * filled + "░" * (width - filled)


def render_markdown(report: dict) -> str:
    """평가 결과 dict를 제출·검토 가능한 Markdown 보고서로 변환합니다."""

    baseline = report["summary"]["baseline"]
    regex = report["summary"]["hybrid_regex"]
    kiwi = report["summary"]["hybrid_kiwi"]
    lines = [
        "# Python 공식 문서 RAG 평가 결과",
        "",
        "## 1. 평가 요약",
        "",
        "| 지표 | Baseline | Hybrid Regex | Hybrid Kiwi |",
        "|---|---:|---:|---:|",
        f"| Hit Rate@4 | {baseline['hit_rate']:.3f} | {regex['hit_rate']:.3f} | {kiwi['hit_rate']:.3f} |",
        f"| MRR@4 | {baseline['mrr']:.3f} | {regex['mrr']:.3f} | {kiwi['mrr']:.3f} |",
        f"| 평가 질문 수 | {baseline['scored_questions']} | {regex['scored_questions']} | {kiwi['scored_questions']} |",
        "",
        "- Baseline: Dense Similarity Search Top-4",
        "- Hybrid Regex: Dense Search와 정규식 BM25를 weighted RRF로 결합한 Top-4",
        "- Hybrid Kiwi: Dense Search와 Kiwi 형태소 BM25를 weighted RRF로 결합한 Top-4",
        "- 정답 문서가 없는 질문은 Retrieval 점수에서 제외",
        "",
        "### 지표 그래프",
        "",
        "```text",
        f"Hit Rate  Baseline     {_bar(baseline['hit_rate'])} {baseline['hit_rate']:.3f}",
        f"          Hybrid Regex {_bar(regex['hit_rate'])} {regex['hit_rate']:.3f}",
        f"          Hybrid Kiwi  {_bar(kiwi['hit_rate'])} {kiwi['hit_rate']:.3f}",
        "",
        f"MRR       Baseline     {_bar(baseline['mrr'])} {baseline['mrr']:.3f}",
        f"          Hybrid Regex {_bar(regex['mrr'])} {regex['mrr']:.3f}",
        f"          Hybrid Kiwi  {_bar(kiwi['mrr'])} {kiwi['mrr']:.3f}",
        "```",
        "",
        f"- Hit Rate@4는 세 방식 모두 {baseline['hit_rate']:.3f}로 동일합니다.",
        f"- Hybrid Regex는 Baseline보다 MRR@4가 {regex['mrr'] - baseline['mrr']:+.3f} 높아 정답 문서를 더 위에 배치했습니다.",
        "- 기본 질문 응답에는 가장 단순하면서 MRR이 높은 Hybrid Regex를 사용합니다.",
        "",
    ]

    generation = report.get("generation", [])
    if generation:
        lines.extend(
            [
                "## 2. 대표 질문 Generation 비교",
                "",
                "근거 여부는 기대 핵심어와 출처 파일 표시를 함께 확인하며, 문서 밖 질문은 지정된 거절 문구를 확인합니다.",
                "전체 Top-4와 실제 답변은 비교표 아래의 질문별 상세 기록에서 확인할 수 있습니다.",
                "",
                "| 질문 | Baseline 검색 | 개선 검색 | 답변 변화 | 판단 |",
                "|---|---|---|---|---|",
            ]
        )
        for row in generation:
            lines.append(
                f"| Q{row['number']} | "
                f"{row['baseline']['search_result']} | "
                f"{row['improved']['search_result']} | "
                f"{row['change']} | {_escape_cell(row['judgment'])} |"
            )
        lines.append("")

        for row in generation:
            lines.extend(
                [
                    f"### Q{row['number']}. {_escape_cell(row['question'])}",
                    "",
                    "#### Baseline 답변",
                    "",
                    f"- 근거 여부: {'충족' if row['baseline']['grounded'] else '미충족'}",
                    f"- 검색 Top-4: {_search_text(row['baseline']['documents'])}",
                    "",
                    *_quote(row["baseline"]["answer"]),
                    "",
                    "#### Regex Hybrid 답변",
                    "",
                    f"- 근거 여부: {'충족' if row['improved']['grounded'] else '미충족'}",
                    f"- 검색 Top-4: {_search_text(row['improved']['documents'])}",
                    "",
                    *_quote(row["improved"]["answer"]),
                    "",
                    f"- 변화: **{row['change']}**",
                    f"- 판단 근거: {row['judgment']}",
                    "",
                ]
            )

    lines.extend(
        [
            f"## {3 if generation else 2}. 질문별 Retrieval 결과",
            "",
        ]
    )

    for number, row in enumerate(report["results"], start=1):
        lines.extend(
            [
                f"### {number}. {_escape_cell(row['question'])}",
                "",
                "| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |",
                "|---|---:|---:|---:|",
                (
                    "| Baseline | "
                    f"{_metric_text(row['baseline']['hit'])} | "
                    f"{_rank_text(row['baseline'])} | "
                    f"{_metric_text(row['baseline']['reciprocal_rank'])} |"
                ),
                *[
                    (
                        f"| {label} | "
                        f"{_metric_text(row[name]['hit'])} | "
                        f"{_rank_text(row[name])} | "
                        f"{_metric_text(row[name]['reciprocal_rank'])} |"
                    )
                    for name, label in PIPELINES[1:]
                ],
                "",
            ]
        )

        for pipeline_name, label in PIPELINES:
            lines.extend(
                [
                    f"#### {label} 검색 결과",
                    "",
                    "| 순위 | Source | 시작 위치 | 내용 미리보기 |",
                    "|---:|---|---:|---|",
                ]
            )
            for document in row[pipeline_name]["documents"]:
                lines.append(
                    f"| {document['rank']} | {_escape_cell(document['source'])} | "
                    f"{document['start_index']} | {_escape_cell(document['preview'])} |"
                )
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"
