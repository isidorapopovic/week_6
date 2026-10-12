from src.chunking import Chunk
import pytest

from src.corpus import load_corpus
from src.chunking import build_chunks
from src.retrieval import retrieve_top_k


def test_retrieve_top_k_orders_by_score_desc() -> None:
    chunks = [
        Chunk(chunk_id="a", doc_id="1", title="A", text="rag retrieval citations evidence"),
        Chunk(chunk_id="b", doc_id="1", title="B", text="weather forecast rain tomorrow"),
    ]
    results = retrieve_top_k("rag citations", chunks, k=2)
    assert results
    assert results[0].chunk.chunk_id == "a"


def test_retrieve_top_k_returns_empty_for_unrelated_query() -> None:
    chunks = [
        Chunk(chunk_id="a", doc_id="1", title="A", text="vector database retrieval"),
    ]
    results = retrieve_top_k("basketball playoffs", chunks, k=2)
    assert results == []


@pytest.mark.parametrize("k, expected_ids", [(2, ["high", "tie-first"]),
                                           (3, ["high", "tie-first", "tie-second"])])
def test_top_k_selects_highest_scores_and_preserves_ties(k, expected_ids) -> None:
    chunks = [
        Chunk("low", "1", "Low", "rag weather rain sun"),
        Chunk("tie-first", "2", "Tie", "RAG, evidence!"),
        Chunk("unrelated", "3", "None", "weather rain"),
        Chunk("high", "4", "High", "rag rag retrieval"),
        Chunk("tie-second", "5", "Tie", "retrieval weather"),
    ]
    results = retrieve_top_k("rag retrieval", chunks, k=k)
    assert [item.chunk.chunk_id for item in results] == expected_ids
    assert [item.score for item in results] == [1.0, 0.5, 0.5][:k]


def test_minimum_score_is_inclusive_and_can_return_fewer_than_k() -> None:
    chunks = [
        Chunk("boundary", "1", "Boundary", "rag weather"),
        Chunk("below", "2", "Below", "rag weather rain"),
        Chunk("empty", "3", "Empty", ""),
    ]
    results = retrieve_top_k("rag", chunks, k=3, min_score=0.5)
    assert [(item.chunk.chunk_id, item.score) for item in results] == [("boundary", 0.5)]


@pytest.mark.parametrize("k", [0, -1])
def test_nonpositive_k_is_rejected(k) -> None:
    with pytest.raises(ValueError, match="k must be > 0"):
        retrieve_top_k("rag", [], k=k)


def test_default_corpus_top_k_matches_hand_calculated_ranking() -> None:
    chunks = build_chunks(load_corpus("default"), chunk_size=140, overlap=30)
    query = "How do chunk size and overlap improve retrieval quality?"
    expected_ids = ["doc-2-chunk-0", "doc-2-chunk-1", "doc-3-chunk-1",
                    "doc-1-chunk-0", "doc-3-chunk-0"]
    full = retrieve_top_k(query, chunks, k=len(chunks))
    assert [item.chunk.chunk_id for item in full] == expected_ids
    assert [item.score for item in full] == pytest.approx([8/20, 1/5, 1/5, 2/18, 2/22])
    for k in (2, 3):
        assert retrieve_top_k(query, chunks, k=k) == full[:k]
