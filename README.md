# AI PR Reviewer for DevOps

A lightweight DevOps-focused pull request reviewer that checks infrastructure and CI/CD files for common reliability, security, and operational issues.

## Checks

- Dockerfile best practices
- GitHub Actions workflow safety
- Terraform security/reliability patterns
- Kubernetes manifest risks
- Missing resource limits and health checks
- Hard-coded secrets and privileged containers

## Project structure

```text
.
├── .github/workflows/ci.yml
├── reviewer/
│   ├── __init__.py
│   ├── checks.py
│   └── cli.py
├── tests/test_checks.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Run locally

```bash
python -m reviewer.cli .
```

## Example

```text
$ python -m reviewer.cli .
AI PR Reviewer
Findings: 0
Review complete.
```

This project is intentionally dependency-light so it can run inside CI without a large runtime footprint.
