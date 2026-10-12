# Task 02: Verified top-k retrieval

Executed on 2026-10-12 with Python 3.13.3. Retrieval implementation unchanged. Reproduce from the repository root:

```powershell
python -m scripts.verify_retrieval
```

## Recorded stdout

```text
Query: How do chunk size and overlap improve retrieval quality?
Corpus: default; chunk_size: 140; overlap: 30; min_score: 0.01
Total chunks: 6

Requested k=6; returned=5
Rank 1: doc-2-chunk-0; score=0.400000; matches=8; tokens=20
Document: doc-2; title: Chunking and Metadata
Text: Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source tra
Rank 2: doc-2-chunk-1; score=0.200000; matches=1; tokens=5
Document: doc-2; title: Chunking and Metadata
Text: helps filtering and source traceability.
Rank 3: doc-3-chunk-1; score=0.200000; matches=1; tokens=5
Document: doc-3; title: Refusal Behavior
Text: ces hallucinations and increases trust.
Rank 4: doc-1-chunk-0; score=0.111111; matches=2; tokens=18
Document: doc-1; title: RAG Fundamentals
Text: Retrieval augmented generation combines retrieval with text generation. The model should answer using retrieved evidence rather than unsuppo
Rank 5: doc-3-chunk-0; score=0.090909; matches=2; tokens=22
Document: doc-3; title: Refusal Behavior
Text: If retrieved context does not support a claim, the system should refuse and ask for better evidence. This reduces hallucinations and increas

Requested k=2; returned=2
Rank 1: doc-2-chunk-0; score=0.400000; matches=8; tokens=20
Document: doc-2; title: Chunking and Metadata
Text: Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source tra
Rank 2: doc-2-chunk-1; score=0.200000; matches=1; tokens=5
Document: doc-2; title: Chunking and Metadata
Text: helps filtering and source traceability.

Requested k=3; returned=3
Rank 1: doc-2-chunk-0; score=0.400000; matches=8; tokens=20
Document: doc-2; title: Chunking and Metadata
Text: Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source tra
Rank 2: doc-2-chunk-1; score=0.200000; matches=1; tokens=5
Document: doc-2; title: Chunking and Metadata
Text: helps filtering and source traceability.
Rank 3: doc-3-chunk-1; score=0.200000; matches=1; tokens=5
Document: doc-3; title: Refusal Behavior
Text: ces hallucinations and increases trust.
```

## Why the ranking is correct

| Rank | Chunk ID | Matching tokens (occurrences) | Token count | Score |
| --- | --- | --- | --- | --- |
| 1 | doc-2-chunk-0 | chunk, size, and, overlap, improve, retrieval, quality, and | 20 | 8/20 = 0.4 |
| 2 | doc-2-chunk-1 | and | 5 | 1/5 = 0.2 |
| 3 | doc-3-chunk-1 | and | 5 | 1/5 = 0.2 |
| 4 | doc-1-chunk-0 | retrieval, retrieval | 18 | 2/18 = 0.111111… |
| 5 | doc-3-chunk-0 | and, and | 22 | 2/22 = 0.090909… |

The sixth chunk, `doc-1-chunk-1`, has zero matching tokens and is excluded by the 0.01 minimum. All five returned results exceed the threshold. Scores are nonincreasing; the 0.2 tie retains the order in which `build_chunks` emitted the chunks. Top-2 and top-3 exactly match the corresponding prefixes of the full five-result ranking. Returning five results for k=6 is correct because only five are eligible.

The first result is substantively relevant and contains the full chunking-quality sentence. Results two and three match only a common word, `and`, and do not answer the question. Increasing k adds lexical matches, not necessarily useful supporting evidence. This task verifies the existing lexical retrieval contract; improving semantic relevance or removing stopwords would be a separate scoring change and would require rerunning Task 01.

## Tests and changes

Added six pytest cases in `tests/test_retrieval.py` (including parameterized cases) to check:

- Highest-scoring selection for k=2 and k=3 from deliberately unsorted input, with stable ties and literal expected scores.
- Inclusive minimum-score filtering, empty chunk handling, and fewer-than-k results.
- Rejection of k=0 and k=-1.
- The default corpus's complete hand-calculated ranking and both top-k prefixes.

No production retrieval changes were required. Added `scripts/verify_retrieval.py` to reproduce the evidence. Corrected Task 02's test command from unittest discovery to pytest; the tests are pytest functions. Corrected Task 01's explanatory token count from 10/25 to 8/20; its recorded score of 0.4 and configuration decision are unchanged.

The initial new corpus test failed because its manually entered fourth/fifth positions and token counts were incorrect. Inspection of actual tokenized text resolved the expectation error; retrieval code was unchanged. Final complete-suite command and stdout:

```powershell
python -m pytest -q
```

```text
...............                                                          [100%]
15 passed in 0.10s
```
