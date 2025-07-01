#!/bin/sh
set -e

ls

echo "Running Alembic migrations..."
alembic -c alembic.ini upgrade head

echo "Starting FastAPI app..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "Starting Telegram bot..."
python -m app.telegram_bot