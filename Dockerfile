FROM python:3.12.10-bookworm

WORKDIR /VoroniniFun
COPY pyproject.toml poetry.lock README.md ./
RUN pip install poetry
RUN poetry install --no-interaction --no-root

COPY . /VoroniniFun
COPY ./app/.env .env

ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1