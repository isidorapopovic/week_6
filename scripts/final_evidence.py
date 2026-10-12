"""Reproduce full retrieval and real CLI stdout for the final evidence pair."""

import subprocess
import sys

from src.chunking import build_chunks
from src.corpus import load_corpus
from src.rag import REFUSAL_MESSAGE, build_grounded_answer
from src.retrieval import retrieve_top_k


def main() -> None:
    cases = (
        ("Supported", "training-rag", "Why are citations important in RAG?", 220, 1, False),
        ("Unsupported", "default", "Who won the world cup in 1958?", 140, 2, True),
    )
    for label, profile, question, size, k, expected_refusal in cases:
        args = ["-m", "src.cli", "--corpus-profile", profile, "--question", question,
                "--chunk-size", str(size), "--overlap", "30", "--top-k", str(k)]
        print(f"=== {label} case ===")
        print(f'Command: python -m src.cli --corpus-profile {profile} --question "{question}" '
              f'--chunk-size {size} --overlap 30 --top-k {k}')
        chunks = build_chunks(load_corpus(profile), chunk_size=size, overlap=30)
        retrieved = retrieve_top_k(question, chunks, k=k)
        print("Retrieved count:", len(retrieved))
        for rank, item in enumerate(retrieved, 1):
            print(f"Rank {rank}: {item.chunk.chunk_id}; score={item.score:.6f}")
            print(f"Document: {item.chunk.doc_id}; title: {item.chunk.title}")
            print("Text:", item.chunk.text)
        result = build_grounded_answer(question, chunks, top_k=k)
        if result.refused != expected_refusal:
            raise RuntimeError(f"Unexpected refusal behavior for {label}")
        if expected_refusal:
            if result.answer != REFUSAL_MESSAGE or result.citations:
                raise RuntimeError("Refusal must use the standard message with no citations")
        else:
            if result.citations != [r.chunk.chunk_id for r in retrieved]:
                raise RuntimeError("Citation IDs do not match retrieval")
            if result.answer.splitlines()[1:] != [
                f"[{r.chunk.chunk_id}] {r.chunk.text}" for r in retrieved
            ]:
                raise RuntimeError("Cited text does not match retrieval")
        completed = subprocess.run([sys.executable, *args], check=True, capture_output=True, text=True)
        if result.answer not in completed.stdout:
            raise RuntimeError("CLI and direct answer differ")
        if f"Refused: {expected_refusal}" not in completed.stdout:
            raise RuntimeError("CLI refusal flag differs")
        expected_citations = ", ".join(result.citations) if result.citations else "None"
        if f"Citations: {expected_citations}\n" not in completed.stdout:
            raise RuntimeError("CLI citations differ")
        print("CLI stdout:")
        print(completed.stdout, end="")
        print("Verification: PASS\n")


if __name__ == "__main__":
    main()
