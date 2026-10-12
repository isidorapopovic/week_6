from src.chunking import build_chunks
from src.corpus import load_default_corpus
from src.rag import build_grounded_answer
import pytest

from src.corpus import load_corpus
from src.retrieval import retrieve_top_k


@pytest.mark.parametrize("size, top_k", [(140, 2), (220, 1)])
def test_training_citations_identify_exact_retrieved_passages(size, top_k) -> None:
    query = "Why are citations important in RAG?"
    chunks = build_chunks(load_corpus("training-rag"), chunk_size=size, overlap=30)
    retrieved = retrieve_top_k(query, chunks, k=top_k)
    result = build_grounded_answer(query, chunks, top_k=top_k)
    assert result.refused is False
    assert result.citations == [item.chunk.chunk_id for item in retrieved]
    assert result.answer.splitlines()[1:] == [
        f"[{item.chunk.chunk_id}] {item.chunk.text}" for item in retrieved
    ]


def test_supported_citation_preserves_complete_explanation() -> None:
    chunks = build_chunks(load_corpus("training-rag"), chunk_size=220, overlap=30)
    result = build_grounded_answer("Why are citations important in RAG?", chunks, top_k=1)
    assert result.citations == ["tr-doc-1-chunk-0"]
    assert "Citations improve transparency and trust because users can verify evidence." in result.answer


def test_cli_separates_answer_and_citations(capsys, monkeypatch) -> None:
    from src.cli import main

    monkeypatch.setattr("sys.argv", ["rag", "--corpus-profile", "training-rag",
        "--question", "Why are citations important in RAG?",
        "--chunk-size", "220", "--overlap", "30", "--top-k", "1"])
    main()
    output = capsys.readouterr().out
    assert "[tr-doc-1-chunk-0] RAG with citations" in output
    assert "\nRefused: False\nCitations: tr-doc-1-chunk-0\n" in output
    assert output.index("Answer:") < output.index("Citations: tr-doc-1-chunk-0")


def test_build_grounded_answer_returns_citations_for_supported_query() -> None:
    chunks = build_chunks(load_default_corpus(), chunk_size=120, overlap=20)
    result = build_grounded_answer("What is retrieval augmented generation?", chunks, top_k=2)
    assert result.refused is False
    assert len(result.citations) >= 1


def test_build_grounded_answer_refuses_unsupported_query() -> None:
    chunks = build_chunks(load_default_corpus(), chunk_size=120, overlap=20)
    result = build_grounded_answer("Who was emperor of Mars?", chunks, top_k=2)
    assert result.refused is True
    assert result.citations == []
