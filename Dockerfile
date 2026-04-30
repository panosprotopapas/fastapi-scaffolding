FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Poetry
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl
    
# App
COPY ./src ./src

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "5000"]
