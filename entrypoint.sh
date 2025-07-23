#!/bin/bash
set -e

echo "Waiting for postgres..."

until nc -z -v -w30 db 5432
do
  echo "Waiting for postgres at db:5432..."
  sleep 1
done

echo "Postgres is up - continuing"

echo "🧠 Making migrations..."
python manage.py makemigrations --noinput

echo "📦 Running migrations..."
python manage.py migrate --noinput

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --log-level debug
