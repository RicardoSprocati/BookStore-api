# Usa imagem base do Python 3.11
FROM python:3.11-slim AS python-base

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Adiciona o poetry e o venv no PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry mais recente
RUN curl -sSL https://install.python-poetry.org | python -

# Define diretório de trabalho para o Python
WORKDIR $PYSETUP_PATH

# Copia arquivos de dependências
COPY pyproject.toml poetry.lock ./ 

# Instala as dependências
RUN poetry install --no-dev

# Copia o restante do código
WORKDIR /app
COPY . /app/

# Expõe a porta
EXPOSE 8000

# Comando padrão usando Gunicorn para produção
CMD ["poetry", "run", "gunicorn", "bookstore.wsgi:application", "--bind", "0.0.0.0:$PORT"]
