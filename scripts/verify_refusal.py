"""Record raw retrieval and final output for Task 04 unsupported cases."""

from src.chunking import build_chunks
from src.corpus import load_corpus
from src.rag import build_grounded_answer
from src.retrieval import retrieve_top_k


def main() -> None:
    chunks = build_chunks(load_corpus("default"), chunk_size=140, overlap=30)
    print("Corpus: default; chunk_size: 140; overlap: 30; top_k: 2")
    for query in ("Who won the world cup in 1958?", "Zanzibar population 2025?"):
        print("\nQuestion:", query)
        retrieved = retrieve_top_k(query, chunks, k=2)
        print("Retrieved count:", len(retrieved))
        for rank, item in enumerate(retrieved, 1):
            print(f"Rank {rank}: {item.chunk.chunk_id}; score={item.score:.6f}")
            print(f"Document: {item.chunk.doc_id}; title: {item.chunk.title}")
            print("Text:", item.chunk.text)
        result = build_grounded_answer(query, chunks, top_k=2)
        print("Answer:", result.answer)
        print("Refused:", result.refused)
        print("Citations:", result.citations)


if __name__ == "__main__":
    main()
