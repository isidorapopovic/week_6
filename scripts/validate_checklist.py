"""Run all evidence and tests using the invoking Python environment."""

import subprocess
import sys


def main() -> None:
    commands = [
        ["--version"],
        ["-m", "pytest", "--version"],
        ["-m", "scripts.compare_chunking"],
        ["-m", "scripts.verify_retrieval"],
        ["-m", "scripts.verify_citations"],
        ["-m", "scripts.verify_refusal"],
        ["-m", "scripts.final_evidence"],
        ["-m", "scripts.verify_scoring_extension"],
        ["-m", "src.cli", "--corpus-profile", "training-rag", "--question",
         "Why are citations important in RAG?", "--chunk-size", "220", "--overlap", "30",
         "--top-k", "1", "--ignore-common-words"],
        ["-m", "pytest", "-q"],
    ]
    for args in commands:
        print("\nCommand:", subprocess.list2cmdline([sys.executable, *args]), flush=True)
        completed = subprocess.run([sys.executable, *args], capture_output=True, text=True)
        print(completed.stdout, end="", flush=True)
        if completed.stderr:
            print(completed.stderr, end="", flush=True)
        if completed.returncode:
            raise SystemExit(completed.returncode)
    print("\nChecklist technical validation: PASS", flush=True)


if __name__ == "__main__":
    main()
