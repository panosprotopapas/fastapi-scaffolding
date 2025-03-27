FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && apt-get install -y curl

COPY ./requirements.txt requirements.txt
RUN pip --disable-pip-version-check install -r requirements.txt

COPY ./src ./src

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "5000"]
