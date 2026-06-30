#!/bin/sh
set -e

echo "Waiting for database..."

until uv run alembic current >/dev/null 2>&1; do
    sleep 2
done

echo "Running migrations..."
uv run alembic upgrade head

echo "Starting FastAPI..."
exec "$@"