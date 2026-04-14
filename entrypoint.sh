#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "PostgreSQL is up - running migrations"
python manage.py migrate

echo "Starting Django Ninja API"
python manage.py runserver 0.0.0.0:${APP_PORT:-8000}
