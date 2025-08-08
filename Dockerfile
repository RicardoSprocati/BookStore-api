# ========= Base =========
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Dependências do sistema (psycopg2, compilação etc.)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     build-essential \
     libpq-dev \
     curl \
  && rm -rf /var/lib/apt/lists/*

# Venv
ENV VENV_PATH=/opt/venv
RUN python -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

# ========= Builder (usa Poetry só para gerar requirements) =========
FROM base AS builder

# Instala Poetry (só no build)
ENV POETRY_HOME=/opt/poetry \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1
RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Copia manifestos do Poetry
COPY pyproject.toml poetry.lock ./

# Exporta requirements e instala (sem dev)
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# ========= Runtime =========
FROM base AS runtime

# Copia libs do builder (venv completo)
COPY --from=builder /opt/venv /opt/venv

# Diretório da app
WORKDIR /app
COPY . /app

# Pasta para estáticos coletados
RUN mkdir -p /app/staticfiles

# Entrypoint: espera o DB, roda migrations, collectstatic e sobe gunicorn
COPY ./docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Ajuste o módulo WSGI se o seu for outro (ex.: config.wsgi)
ENV DJANGO_WSGI=bookstore.wsgi:application

CMD ["/entrypoint.sh"]
