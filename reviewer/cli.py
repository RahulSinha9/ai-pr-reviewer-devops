"""Command-line entry point for the DevOps reviewer."""

from pathlib import Path
import argparse

from .checks import review_tree


def main() -> int:
    parser = argparse.ArgumentParser(description="Review DevOps files for common risks")
    parser.add_argument("path", nargs="?", default=".", help="Repository path")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    findings = review_tree(root)

    print("AI PR Reviewer")
    print(f"Files scanned: {sum(1 for p in root.rglob('*') if p.is_file())}")
    print(f"Findings: {len(findings)}")
    for filename, finding in findings:
        print(f"- {filename}: {finding}")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
