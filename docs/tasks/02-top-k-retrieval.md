# Outcome 2: Top-k retrieval

## Task

Verify that `src/retrieval.py` returns relevant chunks in descending score order, with examples for `k=2` and `k=3`.

## Repository behavior

`tokenize` extracts lowercase ASCII alphanumeric tokens. `lexical_score` counts occurrences of chunk tokens that belong to the unique query-token set, then divides by the number of chunk tokens. Repeated matching words in a chunk count repeatedly. `retrieve_top_k` filters scores below `min_score=0.01`, sorts descending, and returns up to `k` results. Equal scores retain input order; fewer than k matches is valid. Nonpositive k raises `ValueError`.

## Procedure

The CLI shows answers and citations but does not print retrieval scores. Run this PowerShell command to capture the full retrieval evidence:

```powershell
@'
from src.corpus import load_corpus
from src.chunking import build_chunks
from src.retrieval import retrieve_top_k, tokenize

query = "How do chunk size and overlap improve retrieval quality?"
chunks = build_chunks(load_corpus("default"), chunk_size=140, overlap=30)
print("Query:", query)
for k in (2, 3):
    results = retrieve_top_k(query, chunks, k=k)
    print("\nTop-k:", k, "Returned:", len(results))
    for rank, item in enumerate(results, 1):
        tokens = tokenize(item.chunk.text)
        matches = sum(token in set(tokenize(query)) for token in tokens)
        print(rank, item.chunk.chunk_id, "score=", item.score,
              "matches=", matches, "tokens=", len(tokens))
        print("Document:", item.chunk.doc_id, "Title:", item.chunk.title)
        print("Text:", item.chunk.text)
'@ | python -

python -m unittest discover -s tests -v
```

Check each reported score against `matches / tokens`. To verify top-k selection as well as ordering, inspect all eligible results with `k=len(chunks)` and confirm the smaller lists are prefixes of that ranking. Discuss semantic relevance separately: common question words may score even when a chunk does not answer the question.

## Evidence worksheet

- Query: TODO
- Corpus and chunk configuration: TODO
- Top-k output (`k=2`): TODO
- Top-k output (`k=3`): TODO
- Full eligible ranking: TODO
- Why ranking is correct under the implemented score: TODO
- Semantic relevance or ranking limitations: TODO
- Test command, output, and any fixes: TODO

## Acceptance checks

- [ ] Both required k values are documented.
- [ ] Scores are nonincreasing and meet the minimum score.
- [ ] Returned count is at most k and selected results lead the full ranking.
- [ ] IDs, text, and score calculations are recorded.
