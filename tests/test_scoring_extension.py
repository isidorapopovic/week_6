import pytest

from src.chunking import Chunk, build_chunks
from src.corpus import load_corpus
from src.retrieval import lexical_score, retrieve_top_k


def test_extension_does_not_reward_common_word_only_matches() -> None:
    assert lexical_score("Who won the cup?", "the the the") == 1.0
    assert lexical_score("Who won the cup?", "the the the", ignore_common_words=True) == 0.0


def test_extension_retains_topic_matches_and_original_denominator() -> None:
    assert lexical_score("What is RAG?", "RAG is retrieval", ignore_common_words=True) == pytest.approx(1/3)


def test_extension_ranks_topic_passage_above_common_word_distractor() -> None:
    chunks = [Chunk("noise", "1", "Noise", "the the the"),
              Chunk("topic", "2", "Topic", "cup football tournament")]
    results = retrieve_top_k("Who won the cup?", chunks, k=2, ignore_common_words=True)
    assert [(r.chunk.chunk_id, r.score) for r in results] == [("topic", 1/3)]


def test_extension_common_word_only_query_returns_no_results() -> None:
    chunks = [Chunk("a", "1", "A", "the and rag")]
    assert retrieve_top_k("the and", chunks, ignore_common_words=True) == []


def test_extension_removes_irrelevant_chunks_from_homework_query() -> None:
    chunks = build_chunks(load_corpus(), chunk_size=140, overlap=30)
    results = retrieve_top_k("How do chunk size and overlap improve retrieval quality?",
                             chunks, k=3, ignore_common_words=True)
    assert [r.chunk.chunk_id for r in results] == ["doc-2-chunk-0", "doc-1-chunk-0"]
    assert [r.score for r in results] == pytest.approx([6/20, 2/18])


def test_extension_cli_flag_uses_improved_scoring(capsys, monkeypatch) -> None:
    from src.cli import main

    monkeypatch.setattr("sys.argv", ["rag", "--question", "Who won the world cup in 1958?",
                                   "--ignore-common-words"])
    main()
    output = capsys.readouterr().out
    assert "Refused: True\nCitations: None" in output
