# Task 03: Citation quality evidence

Executed on 2026-10-12 with Python 3.13.3. Corpus and RAG implementation unchanged. Both the suggested baseline and the final supported configuration were tested. Chunk IDs refer to the settings of each run.

## Reproduce retrieval and citation verification

```powershell
python -m scripts.verify_citations
```

Recorded stdout:

```text
Question: Why are citations important in RAG?
Corpus: training-rag; overlap: 30

Configuration: chunk_size=140; top_k=2
Rank 1: tr-doc-1-chunk-0; score=0.210526
Document: tr-doc-1; title: RAG with Citations
Text: RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transpare
Rank 2: tr-doc-4-chunk-1; score=0.125000
Document: tr-doc-4; title: Refusal and Grounding
Text: educes hallucinations and aligns with safe RAG practice.
Answer:
Grounded response based on retrieved context:
[tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transpare
[tr-doc-4-chunk-1] educes hallucinations and aligns with safe RAG practice.
Refused: False
Citations: tr-doc-1-chunk-0, tr-doc-4-chunk-1
IDs match retrieval: True
Cited lines match source text: True

Configuration: chunk_size=220; top_k=1
Rank 1: tr-doc-1-chunk-0; score=0.153846
Document: tr-doc-1; title: RAG with Citations
Text: RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.
Answer:
Grounded response based on retrieved context:
[tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.
Refused: False
Citations: tr-doc-1-chunk-0
IDs match retrieval: True
Cited lines match source text: True
```

## Supported CLI command and output

```powershell
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 220 --overlap 30 --top-k 1
```

```text
Question:
Why are citations important in RAG?

Answer:
Grounded response based on retrieved context:
[tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.

Corpus profile: training-rag

Refused: False
Citations: tr-doc-1-chunk-0
```

## Citation and grounding assessment

| Check | Observed result |
| --- | --- |
| Inline citation belongs to retrieval | `tr-doc-1-chunk-0` is the sole retrieved result |
| Separate citation list matches inline citation | Both contain exactly `tr-doc-1-chunk-0` |
| Cited text matches source | Exact full chunk text after the bracketed ID |
| Passage answers the question | Explains transparency, trust, and user verification |
| Answer and citations are separate | CLI prints answer body, then a separate `Citations:` field |
| Supported case accepted | `Refused: False` |

The 140/30, top-k 2 baseline also maps citations correctly, but its first result ends at `transpare` and omits the reason users can verify evidence. Its second result discusses safe RAG practice and matches `RAG`, without explaining citation value. Citation correctness alone is therefore insufficient to assess answer usefulness.

For this supported case, chunk size 220 keeps the full citation document together; top-k 1 uses that directly relevant source without appending a weakly related result. Its lower lexical score reflects the longer passage, while its text offers better support. The global 140/30 defaults retained in Task 01 are unchanged: this is a different corpus and query, with explicit local settings. Because both size and top-k changed here, this comparison assesses the resulting citation evidence, not an isolated causal effect of either parameter.

The answer generator copies retrieved text with inline chunk IDs; it does not synthesize an LLM answer. No factual claims were added beyond the supplied source. Tests establish citation mapping and formatting for these cases, not general semantic relevance or refusal reliability. Refusal work remains Task 04.

## Changes and tests

Added a reproducible verification script and four pytest cases: two parameterized configurations check exact retrieval-to-citation mapping and copied text; one checks the full explanation survives; one runs the CLI and checks its separate citations field. No changes to `src/rag.py` or global defaults were necessary. Corrected Task 03's test command from unittest to pytest.

```powershell
python -m pytest -q
```

Recorded complete-suite stdout:

```text
...................                                                      [100%]
19 passed in 0.09s
```
