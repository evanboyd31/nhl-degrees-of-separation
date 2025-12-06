#!/bin/sh
set -e
. /app/.venv/bin/activate
exec uvicorn app.main:app --host 0.0.0.0 --port 8005