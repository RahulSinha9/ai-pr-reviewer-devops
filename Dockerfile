FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY reviewer ./reviewer
COPY README.md .

RUN useradd --create-home --uid 10001 appuser
USER appuser

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import reviewer"

ENTRYPOINT ["python", "-m", "reviewer.cli"]
CMD ["."]
