"""Reproduce Task 03 retrieval and citation evidence, including the baseline."""

from src.chunking import build_chunks
from src.corpus import load_corpus
from src.rag import build_grounded_answer
from src.retrieval import retrieve_top_k


def main() -> None:
    query = "Why are citations important in RAG?"
    print("Question:", query)
    print("Corpus: training-rag; overlap: 30")
    for size, k in ((140, 2), (220, 1)):
        print(f"\nConfiguration: chunk_size={size}; top_k={k}")
        chunks = build_chunks(load_corpus("training-rag"), chunk_size=size, overlap=30)
        retrieved = retrieve_top_k(query, chunks, k=k)
        for rank, item in enumerate(retrieved, 1):
            print(f"Rank {rank}: {item.chunk.chunk_id}; score={item.score:.6f}")
            print(f"Document: {item.chunk.doc_id}; title: {item.chunk.title}")
            print("Text:", item.chunk.text)
        result = build_grounded_answer(query, chunks, top_k=k)
        print("Answer:")
        print(result.answer)
        print("Refused:", result.refused)
        print("Citations:", ", ".join(result.citations))
        print("IDs match retrieval:", result.citations == [r.chunk.chunk_id for r in retrieved])
        print("Cited lines match source text:", result.answer.splitlines()[1:] == [
            f"[{r.chunk.chunk_id}] {r.chunk.text}" for r in retrieved
        ])


if __name__ == "__main__":
    main()
