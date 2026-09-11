from pathlib import Path

from reviewer.checks import review_file


def test_dockerfile_requires_user_and_healthcheck(tmp_path: Path):
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text("FROM python:3.12-slim\nCMD [\"python\"]\n", encoding="utf-8")

    findings = review_file(dockerfile)

    assert any("non-root USER" in item for item in findings)
    assert any("HEALTHCHECK" in item for item in findings)


def test_example_secret_file_is_ignored(tmp_path: Path):
    config = tmp_path / "config.example"
    config.write_text("API_KEY=example-only-value\n", encoding="utf-8")

    assert not any("secret" in item.lower() for item in review_file(config))
