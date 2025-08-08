#!/usr/bin/env bash
set -e

# Espera opcional pelo DB (pode usar pg_isready; assumindo host $DB_HOST)
if [ -n "$DB_HOST" ]; then
  echo "Aguardando banco em $DB_HOST:$DB_PORT..."
  for i in {1..30}; do
    if pg_isready -h "$DB_HOST" -p "${DB_PORT:-5432}" >/dev/null 2>&1; then
      echo "DB está pronto."
      break
    fi
    sleep 1
  done
fi

echo "Aplicando migrações..."
python manage.py migrate --noinput

echo "Coletando estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
# Ajuste DJANGO_WSGI via env se necessário (ex.: config.wsgi:application)
exec gunicorn "$DJANGO_WSGI" --bind 0.0.0.0:8000 --workers 3 --timeout 60
