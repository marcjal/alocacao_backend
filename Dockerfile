# Stage 1: builder
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update \
 && apt-get install -y build-essential libpq-dev gcc \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: runtime
FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir gunicorn

COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin       /usr/local/bin
COPY --from=builder /app                  /app

RUN useradd --create-home appuser
USER appuser

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=alocacao_backend.settings \
    DATABASE_URL=postgres://aloc:senha@db:5432/alocacao

EXPOSE 8000

CMD ["gunicorn", "alocacao_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
