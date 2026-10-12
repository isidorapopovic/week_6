"""Compare original and optional common-word-filtered lexical scoring."""

from src.chunking import build_chunks
from src.corpus import load_corpus
from src.retrieval import retrieve_top_k


def main() -> None:
    chunks = build_chunks(load_corpus(), chunk_size=140, overlap=30)
    print("Corpus: default; chunk_size: 140; overlap: 30; top_k: 3")
    for query in ("How do chunk size and overlap improve retrieval quality?",
                  "Who won the world cup in 1958?"):
        print("\nQuestion:", query)
        for enabled in (False, True):
            results = retrieve_top_k(query, chunks, k=3, ignore_common_words=enabled)
            print(f"ignore_common_words={enabled}; returned={len(results)}")
            for item in results:
                print(f"{item.chunk.chunk_id}; score={item.score:.6f}; text={item.chunk.text}")


if __name__ == "__main__":
    main()
