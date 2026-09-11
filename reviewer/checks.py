"""Static checks for common DevOps pull-request risks."""

from pathlib import Path
import re

SECRET_PATTERNS = [
    re.compile(r"(?i)(aws_access_key_id|api[_-]?key|password|secret)\s*[:=]\s*[\"']?[A-Za-z0-9_/+=.-]{8,}"),
]


def review_file(path: Path) -> list[str]:
    """Return findings for a single text file."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    findings: list[str] = []
    name = path.name.lower()
    suffix = path.suffix.lower()

    for pattern in SECRET_PATTERNS:
        if pattern.search(text) and not name.endswith(".example"):
            findings.append("Potential hard-coded secret detected.")
            break

    if name == "dockerfile":
        if "USER " not in text.upper():
            findings.append("Dockerfile does not define a non-root USER.")
        if "HEALTHCHECK" not in text.upper():
            findings.append("Dockerfile has no HEALTHCHECK instruction.")

    if suffix in {".yml", ".yaml"} and ".github/workflows" in str(path).replace("\\", "/"):
        if "permissions:" not in text:
            findings.append("GitHub Actions workflow does not declare explicit permissions.")
        if "pull_request_target" in text:
            findings.append("Review pull_request_target carefully: untrusted PR code can become a security risk.")

    if suffix in {".yml", ".yaml"} and "kind: deployment" in text.lower():
        if "resources:" not in text:
            findings.append("Kubernetes Deployment has no resource requests/limits.")

    return findings


def review_tree(root: Path) -> list[tuple[str, str]]:
    """Review supported text files below root and return (file, finding)."""
    results: list[tuple[str, str]] = []
    ignored = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in ignored for part in path.parts):
            continue
        for finding in review_file(path):
            results.append((str(path.relative_to(root)), finding))
    return results
