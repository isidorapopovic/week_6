"""Reproduce the Outcome 1 comparison without changing corpus or ranking."""

from src.chunking import build_chunks
from src.corpus import load_corpus
from src.retrieval import retrieve_top_k


def main() -> None:
    query = "How do chunk size and overlap improve retrieval quality?"
    print("Query:", query)
    print("Corpus: default; top_k: 2; min_score: 0.01")
    for label, size, overlap in (("A", 140, 30), ("B", 80, 20)):
        chunks = build_chunks(load_corpus("default"), chunk_size=size, overlap=overlap)
        print(f"\nConfig {label}: chunk_size={size}, overlap={overlap}, step={size - overlap}")
        print("Total chunks:", len(chunks))
        print("All chunk boundaries:")
        for chunk in chunks:
            print(f"  {chunk.chunk_id} ({len(chunk.text)} characters): {chunk.text!r}")
        print("Top-k retrieval:")
        for rank, result in enumerate(retrieve_top_k(query, chunks, k=2), 1):
            chunk = result.chunk
            print(f"  Rank {rank}: {chunk.chunk_id}; score={result.score:.6f}")
            print(f"  Document: {chunk.doc_id}; title: {chunk.title}")
            print(f"  Text: {chunk.text}")


if __name__ == "__main__":
    main()
