# Checklist completion: installation and optional extension

Validated on 2026-10-12. This closes the technical gaps identified in the checklist audit. Personal understanding, pair contributions, and demo lead remain awaiting learner input.

## Exact pinned installation

Created a new isolated environment rather than changing the existing user Python installation:

```powershell
python -m venv .venv-checklist
.\.venv-checklist\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-checklist\Scripts\python.exe -m scripts.validate_checklist
```

Installation succeeded with `pytest==8.3.3`, plus its dependencies. The validation transcript confirms Python 3.13.3 and pytest 8.3.3. The environment is ignored by Git.

[Full recorded validation stdout](checklist-validation.txt) includes all Outcomes 1–5 evidence scripts, the extension comparison, a supported CLI run with the extension enabled, and the complete test suite:

```text
..................................                                       [100%]
34 passed in 0.14s

Checklist technical validation: PASS
```

## Requested optional extension: improved lexical scoring

Added `ignore_common_words=True` to `lexical_score`, `retrieve_top_k`, and `build_grounded_answer`, exposed through the CLI as `--ignore-common-words`. This excludes the shared set of common grammatical/question words from query matches while retaining the original chunk-token denominator, thresholds, descending order, and stable ties. Defaults retain the original score so previously recorded tasks remain reproducible. The refusal guard and scorer share the same word list.

```powershell
python -m scripts.verify_scoring_extension
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 220 --overlap 30 --top-k 1 --ignore-common-words
```

For the chunking query, original top-3 scores are 0.4, 0.2, 0.2; the latter two match only `and`. The extension removes those two chunks, returning `doc-2-chunk-0` (6/20 = 0.3) and `doc-1-chunk-0` (2/18 = 0.111111). For the unsupported World Cup query, original retrieval returns two passages matching only `the`; the extension returns zero. The supported citation query still produces the complete grounded passage and correct citation.

Added six tests, exceeding the checklist's three-test minimum:

1. Common-word-only passages score zero with the extension.
2. Topic matches retain a hand-calculated score and original denominator.
3. A topic passage outranks a common-word distractor.
4. A common-word-only question returns no results.
5. The homework query excludes its two common-word-only distractors.
6. The CLI accepts the extension flag and refuses the unsupported case.

This improves lexical relevance for these examples; it is not a semantic-entailment check. It can return fewer than k results and can miss paraphrases with no shared content words. All pre-extension tests remain passing.

## Outstanding learner items

- Confirm understanding of source locations and behavior.
- Provide both members' actual names/contributions or confirm individual work.
- Identify the designated Week 6 demo lead.

Only these personal checklist items remain unchecked. No claims about learner understanding or contributions have been invented.
