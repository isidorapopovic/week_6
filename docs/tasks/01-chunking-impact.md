# Outcome 1: Chunking impact

## Task

Tune the chunking parameters used by `src/chunking.py` and compare retrieval quality for the same query. The CLI exposes both parameters, so you can compare configurations without editing defaults first.

## Repository behavior

`split_text_with_overlap` normalizes whitespace and slices by characters, not tokens or sentences. Its step is `chunk_size - overlap`; it can split words. `build_chunks` assigns IDs such as `doc-1-chunk-0`. IDs can refer to different text when the configuration changes.

## Procedure

Use the default corpus, the same question, and `top_k=2` in both runs:

```powershell
python -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 140 --overlap 30 --top-k 2
python -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 80 --overlap 20 --top-k 2
```

Capture scored retrieval for each configuration using the procedure in [Outcome 2](02-top-k-retrieval.md), changing only `chunk_size` and `overlap`. Compare complete ideas retained, broken words, duplicate context, relevant text returned, and scores. A higher lexical score alone does not prove better answer quality.

If you adopt new defaults, update both chunking function defaults and the CLI defaults consistently, then run the existing tests.

## Completed evidence (2026-10-12)

- Config A: `chunk_size=140, overlap=30`, step 110; 6 chunks.
- Config B: `chunk_size=80, overlap=20`, step 60; 9 chunks.
- Fixed query: `How do chunk size and overlap improve retrieval quality?`; corpus: `default`; top-k: 2; minimum score: 0.01.
- Retrieved IDs, scores, text, complete chunk boundaries, and CLI outputs: [recorded experiment](../evidence/task-01-chunking-impact.md).
- Retrieval difference summary: A ranks `doc-2-chunk-0` (0.400000) then `doc-2-chunk-1` (0.200000). B ranks `doc-2-chunk-1` (0.500000) then `doc-2-chunk-0` (0.333333). Both retrieve the chunking document, but B splits the key sentence across chunks, and its first result begins with `e and overlap`. A keeps the sentence intact in its first result. Neither configuration avoids all broken words or duplicate context.
- Chosen configuration: retain A (`140/30`) because its first result preserves the complete claim about chunk size, overlap, and retrieval quality. B's higher matching-token density does not compensate for the lost context in this example. This conclusion is limited to the tested corpus and question.
- Source changes: added `scripts/compare_chunking.py` to reproduce the comparison; retained both chunking and CLI defaults after evaluating the alternative. No retrieval or answer logic changes were needed for this task.
- Validation: `python -m pytest -q` returned `9 passed in 0.05s`. The repository uses pytest tests; use pytest rather than unittest discovery.

## Acceptance checks

- [x] Both configurations were run with the same query, corpus, and top-k.
- [x] Evidence includes actual retrieved text as well as IDs and scores.
- [x] Explanation links observed differences to chunk boundaries and overlap.
- [x] Limitations of character slicing and lexical scoring are acknowledged.
