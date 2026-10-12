# Week 6 RAG evidence

Status: Outcomes 1–4 completed on 2026-10-12. Outcome 5 remains pending.

1. **Outcome 1: Chunking impact**
   - Config A: `chunk_size=140, overlap=30`; 6 chunks; top results `doc-2-chunk-0` (0.400000), `doc-2-chunk-1` (0.200000).
   - Config B: `chunk_size=80, overlap=20`; 9 chunks; top results `doc-2-chunk-1` (0.500000), `doc-2-chunk-0` (0.333333).
   - Retrieval difference summary: same query, default corpus, and top-k 2. A preserves the complete sentence about chunk size and overlap in its first result; B splits it and ranks a mid-word continuation first despite a higher lexical score. Retain A's defaults. Both exhibit word splits and duplicate context. [Full commands, retrieval text, CLI output, analysis, and passing test snapshot](docs/evidence/task-01-chunking-impact.md).
2. **Outcome 2: Top-k retrieval**
   - Query: `How do chunk size and overlap improve retrieval quality?`; default corpus; chunk size 140; overlap 30; minimum score 0.01.
   - Top-k output: k=2 returns `doc-2-chunk-0` (0.4), `doc-2-chunk-1` (0.2); k=3 additionally returns `doc-3-chunk-1` (0.2). [Full retrieval text, score calculations, reproducible command, and test evidence](docs/evidence/task-02-top-k-retrieval.md).
   - Why ranking is correct: scores decrease as 8/20, 1/5, 1/5, 2/18, 2/22 across the full eligible ranking. Equal scores retain input order. Top-2 and top-3 are prefixes of that ranking. Matches to `and` produce semantically weak results; this verifies lexical ranking, not universal relevance.
3. **Outcome 3: Citation quality**
   - Supported query: `Why are citations important in RAG?`; training-rag corpus; chunk size 220; overlap 30; top-k 1.
   - Answer with citations: `[tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.` [Full answer, CLI output, baseline comparison, and passing tests](docs/evidence/task-03-citation-quality.md).
   - Retrieved chunk IDs: `tr-doc-1-chunk-0` (score 0.153846). Inline ID, separate citations list, and complete source text agree; `Refused: False`.
4. **Outcome 4: Refusal behavior**
   - Unsupported query: `Who won the world cup in 1958?`; default corpus; chunk size 140; overlap 30; top-k 2. Also tested `Zanzibar population 2025?` with the same settings.
   - Retrieved context: World Cup returns `doc-1-chunk-0` (0.055556), `doc-3-chunk-0` (0.045455), matching only `the`; Zanzibar returns no chunks. [Full context, before/after evidence, commands, and tests](docs/evidence/task-04-refusal-behavior.md).
   - Refusal output: `I do not have enough grounded evidence in the provided corpus to answer that question.` Both cases return `Refused: True` and no citations after the common-word-only support check was added. This lexical guard does not prove semantic support for every accepted question.
5. **Outcome 5: Final evidence pair**
   - Supported case command + output: TODO — Task 05 pending.
   - Unsupported case command + output: TODO
