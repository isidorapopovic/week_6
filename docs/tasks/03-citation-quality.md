# Outcome 3: Citation quality

## Task

Verify that `src/rag.py` produces grounded output with explicit citations to retrieved chunk IDs.

## Repository behavior

`build_grounded_answer` retrieves chunks and, when it accepts the evidence, copies each retrieved chunk into a line prefixed by `[chunk_id]`. It also returns the IDs in `RagAnswer.citations`. This is an extractive demonstration, not an LLM-generated synthesis. The CLI prints the answer separately from its `Citations:` field.

## Procedure

```powershell
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 140 --overlap 30 --top-k 2
python -m pytest -q
```

Use the retrieval command in [Outcome 2](02-top-k-retrieval.md) with this query and `load_corpus("training-rag")` to capture IDs, scores, metadata, and full text. Check that every bracketed ID in the answer belongs to the retrieved set, and that the separate citations list matches the answer's IDs. Compare each cited line with its source text. Assess whether the retrieved passages actually explain the value of citations; correct IDs alone do not establish relevance.

## Completed evidence (2026-10-12)

- Supported query: `Why are citations important in RAG?`
- Corpus: `training-rag`; final evidence configuration: chunk size 220, overlap 30, top-k 1. Also verified the suggested baseline (140/30, top-k 2).
- Answer with citations, retrieval scores, source metadata, and complete text: [recorded citation verification](../evidence/task-03-citation-quality.md).
- Final retrieved/cited ID: `tr-doc-1-chunk-0`; score 0.153846; title `RAG with Citations`.
- Separate citations field: `Citations: tr-doc-1-chunk-0`.
- Verification: all answer IDs match retrieved IDs in order, and every cited line exactly reproduces its source text. The final passage states that citations improve transparency and trust because users can verify evidence. The baseline has valid citation mapping but truncates that explanation and adds a weakly related refusal passage. Larger chunks and top-k 1 give complete support for this case; this is a local evidence configuration, not a change to global defaults or a claim of universal relevance.
- Changes: added `scripts/verify_citations.py`, four citation/CLI test cases, and full evidence. Retained `src/rag.py` because existing output already meets the citation contract. Corrected the test command to pytest.
- Tests: `python -m pytest -q` — `19 passed in 0.09s`.

## Acceptance checks

- [x] Supported case reports `Refused: False`.
- [x] Answer includes explicit chunk IDs and a separate citations field.
- [x] All citation IDs correspond to retrieved chunks for this configuration.
- [x] Cited text supports the response and no unsupported claims were added.
