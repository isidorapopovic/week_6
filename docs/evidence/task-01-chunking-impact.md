# Task 01: Recorded chunking experiment

Executed on 2026-10-12 with Python 3.13.3. Commands run from the repository root. Retrieval and corpus source were unchanged; both runs used `default`, top-k 2, and minimum score 0.01.

## Reproduce scored retrieval and boundaries

```powershell
python -m scripts.compare_chunking
```

Recorded stdout:

```text
Query: How do chunk size and overlap improve retrieval quality?
Corpus: default; top_k: 2; min_score: 0.01

Config A: chunk_size=140, overlap=30, step=110
Total chunks: 6
All chunk boundaries:
  doc-1-chunk-0 (140 characters): 'Retrieval augmented generation combines retrieval with text generation. The model should answer using retrieved evidence rather than unsuppo'
  doc-1-chunk-1 (47 characters): 'd evidence rather than unsupported assumptions.'
  doc-2-chunk-0 (140 characters): 'Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source tra'
  doc-2-chunk-1 (40 characters): 'helps filtering and source traceability.'
  doc-3-chunk-0 (140 characters): 'If retrieved context does not support a claim, the system should refuse and ask for better evidence. This reduces hallucinations and increas'
  doc-3-chunk-1 (39 characters): 'ces hallucinations and increases trust.'
Top-k retrieval:
  Rank 1: doc-2-chunk-0; score=0.400000
  Document: doc-2; title: Chunking and Metadata
  Text: Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source tra
  Rank 2: doc-2-chunk-1; score=0.200000
  Document: doc-2; title: Chunking and Metadata
  Text: helps filtering and source traceability.

Config B: chunk_size=80, overlap=20, step=60
Total chunks: 9
All chunk boundaries:
  doc-1-chunk-0 (80 characters): 'Retrieval augmented generation combines retrieval with text generation. The mode'
  doc-1-chunk-1 (80 characters): 'generation. The model should answer using retrieved evidence rather than unsuppo'
  doc-1-chunk-2 (36 characters): 'rather than unsupported assumptions.'
  doc-2-chunk-0 (80 characters): 'Chunking splits documents into smaller parts. Good chunk size and overlap improv'
  doc-2-chunk-1 (80 characters): 'e and overlap improve retrieval quality. Metadata helps filtering and source tra'
  doc-2-chunk-2 (30 characters): 'ering and source traceability.'
  doc-3-chunk-0 (79 characters): 'If retrieved context does not support a claim, the system should refuse and ask'
  doc-3-chunk-1 (80 characters): 'ould refuse and ask for better evidence. This reduces hallucinations and increas'
  doc-3-chunk-2 (29 characters): 'inations and increases trust.'
Top-k retrieval:
  Rank 1: doc-2-chunk-1; score=0.500000
  Document: doc-2; title: Chunking and Metadata
  Text: e and overlap improve retrieval quality. Metadata helps filtering and source tra
  Rank 2: doc-2-chunk-0; score=0.333333
  Document: doc-2; title: Chunking and Metadata
  Text: Chunking splits documents into smaller parts. Good chunk size and overlap improv
```

## Config A CLI command and output

```powershell
python -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 140 --overlap 30 --top-k 2
```

```text
Question:
How do chunk size and overlap improve retrieval quality?

Answer:
Grounded response based on retrieved context:
[doc-2-chunk-0] Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source tra
[doc-2-chunk-1] helps filtering and source traceability.

Corpus profile: default

Refused: False
Citations: doc-2-chunk-0, doc-2-chunk-1
```

## Config B CLI command and output

```powershell
python -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 80 --overlap 20 --top-k 2
```

```text
Question:
How do chunk size and overlap improve retrieval quality?

Answer:
Grounded response based on retrieved context:
[doc-2-chunk-1] e and overlap improve retrieval quality. Metadata helps filtering and source tra
[doc-2-chunk-0] Chunking splits documents into smaller parts. Good chunk size and overlap improv

Corpus profile: default

Refused: False
Citations: doc-2-chunk-1, doc-2-chunk-0
```

## Interpretation and decision

| Observation | Config A | Config B |
| --- | --- | --- |
| Chunk count | 6 | 9 |
| Best score | 10 matching tokens / 25 tokens = 0.4 | 7 matching tokens / 14 tokens = 0.5 |
| Second score | 1 / 5 = 0.2 | 5 / 15 = 0.333333 |
| Key sentence intact in first result | Yes | No |
| Fragment examples | `source tra`, `d evidence` | `improv`, `e and overlap`, `ering` |
| Duplicated retrieved context | `helps filtering and source tra` | `e and overlap improv` |

Retain A's existing defaults in `src/chunking.py` and `src/cli.py`. Its first result contains the entire sentence `Good chunk size and overlap improve retrieval quality.` B increases matching-token density but separates `chunk size` from `improve retrieval quality` and ranks the continuation before the beginning. B's 20-character overlap retains some shared text, but does not keep that complete sentence in either chunk. A's 30-character overlap also duplicates text, so some of the two-result context budget is redundant.

Both settings slice words and both retrieve a second passage partly because `and` appears in the question. Scores reflect lexical density rather than semantic support. The corpus states that chunk size and overlap improve quality but does not explain the mechanism; the CLI copies context rather than producing a detailed explanation. This single-query comparison supports the configuration choice for this example, not a universal optimum. Chunk IDs must be interpreted together with their configuration because their text changes between runs.

## Existing test suite

```powershell
python -m pytest -q
```

```text
.........                                                                [100%]
9 passed in 0.05s
```
