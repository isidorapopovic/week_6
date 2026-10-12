# Week 6 RAG evidence

Status: Outcome 1 completed on 2026-10-12. Outcomes 2–5 remain pending; Task 01 outputs do not establish their completion.

1. **Outcome 1: Chunking impact**
   - Config A: `chunk_size=140, overlap=30`; 6 chunks; top results `doc-2-chunk-0` (0.400000), `doc-2-chunk-1` (0.200000).
   - Config B: `chunk_size=80, overlap=20`; 9 chunks; top results `doc-2-chunk-1` (0.500000), `doc-2-chunk-0` (0.333333).
   - Retrieval difference summary: same query, default corpus, and top-k 2. A preserves the complete sentence about chunk size and overlap in its first result; B splits it and ranks a mid-word continuation first despite a higher lexical score. Retain A's defaults. Both exhibit word splits and duplicate context. [Full commands, retrieval text, CLI output, analysis, and passing test snapshot](docs/evidence/task-01-chunking-impact.md).
2. **Outcome 2: Top-k retrieval**
   - Query: TODO — Task 02 pending.
   - Top-k output: TODO
   - Why ranking is correct: TODO
3. **Outcome 3: Citation quality**
   - Supported query: TODO — Task 03 pending.
   - Answer with citations: TODO
   - Retrieved chunk IDs: TODO
4. **Outcome 4: Refusal behavior**
   - Unsupported query: TODO — Task 04 pending.
   - Retrieved context: TODO
   - Refusal output: TODO
5. **Outcome 5: Final evidence pair**
   - Supported case command + output: TODO — Task 05 pending.
   - Unsupported case command + output: TODO
