FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /src

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-traditional && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.in-project true
RUN poetry install --only main

COPY ./app ./app
COPY ./alembic.ini ./alembic.ini
COPY ./tests ./tests

RUN mkdir ./logs

CMD export APP_VERSION=`poetry version -s` && \
    poetry run alembic upgrade head && \
    poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
