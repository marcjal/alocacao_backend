# Stage 1: builder
FROM python:3.11-slim AS builder
WORKDIR /app
# Instala build deps se precisar de psycopg2, etc.
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY . .

# Stage 2: runtime
FROM python:3.11-slim
WORKDIR /app
# Cria usuário sem root
RUN useradd --create-home appuser
USER appuser

# Copia do builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=alocacao_backend.settings \
    DATABASE_URL=postgres://aloc:senha@db:5432/alocacao

# Coleta estáticos (se usar)
# RUN python manage.py collectstatic --noinput

# Expõe porta
EXPOSE 8000

# Comando de execução
CMD ["gunicorn", "alocacao_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
