#!/bin/bash

set -e

until pg_isready -h db; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

alembic upgrade head

exec "$@"