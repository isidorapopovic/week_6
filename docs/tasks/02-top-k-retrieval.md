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

python -m pytest -q
```

Check each reported score against `matches / tokens`. To verify top-k selection as well as ordering, inspect all eligible results with `k=len(chunks)` and confirm the smaller lists are prefixes of that ranking. Discuss semantic relevance separately: common question words may score even when a chunk does not answer the question.

## Completed evidence (2026-10-12)

- Query: `How do chunk size and overlap improve retrieval quality?`
- Corpus and chunk configuration: default; `chunk_size=140`, `overlap=30`, `min_score=0.01`.
- Top-k output (`k=2`): `doc-2-chunk-0` (0.4), `doc-2-chunk-1` (0.2).
- Top-k output (`k=3`): the same two results followed by `doc-3-chunk-1` (0.2).
- Full eligible ranking: [full text, scores, commands, and verification](../evidence/task-02-top-k-retrieval.md).
- Why ranking is correct: descending matching-token density; equal scores preserve corpus/chunk order. Both shorter lists are prefixes of the full eligible ranking.
- Semantic relevance limitation: second and third results match only `and`; the third result is about refusal, not chunking. Correct numerical ordering does not guarantee all returned chunks answer the question.
- Changes: added a reproducible evidence script and six test cases covering exact scores, top-2/top-3 selection, ties, filtering boundaries, fewer-than-k results, invalid k, and the fixed corpus ranking. Retrieval implementation retained because it satisfies its current scoring contract. Corrected the test runner here to pytest and Task 01's best-score token counts to 8/20 (score unchanged).
- Test command: `python -m pytest -q`; final output is recorded in the linked evidence after execution.

## Acceptance checks

- [x] Both required k values are documented.
- [x] Scores are nonincreasing and meet the minimum score.
- [x] Returned count is at most k and selected results lead the full ranking.
- [x] IDs, text, and score calculations are recorded.
