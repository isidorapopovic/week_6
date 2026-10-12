"""Print the fixed Task 02 query's full ranking and top-k evidence."""

from src.chunking import build_chunks
from src.corpus import load_corpus
from src.retrieval import retrieve_top_k, tokenize


def main() -> None:
    query = "How do chunk size and overlap improve retrieval quality?"
    chunks = build_chunks(load_corpus("default"), chunk_size=140, overlap=30)
    print("Query:", query)
    print("Corpus: default; chunk_size: 140; overlap: 30; min_score: 0.01")
    print("Total chunks:", len(chunks))
    query_tokens = set(tokenize(query))
    for k in (len(chunks), 2, 3):
        results = retrieve_top_k(query, chunks, k=k)
        print(f"\nRequested k={k}; returned={len(results)}")
        for rank, result in enumerate(results, 1):
            tokens = tokenize(result.chunk.text)
            matches = sum(token in query_tokens for token in tokens)
            print(f"Rank {rank}: {result.chunk.chunk_id}; "
                  f"score={result.score:.6f}; matches={matches}; tokens={len(tokens)}")
            print(f"Document: {result.chunk.doc_id}; title: {result.chunk.title}")
            print("Text:", result.chunk.text)


if __name__ == "__main__":
    main()
