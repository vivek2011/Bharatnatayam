#!/bin/sh

if [ -n "$SQL_HOST" ] && [ -n "$SQL_PORT" ]; then
    echo "Waiting for postgres ($SQL_HOST:$SQL_PORT)..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
else
    echo "SQL_HOST or SQL_PORT not defined, skipping wait check."
fi

# Run migrations and collect static files
echo "==> Running Django database migrations..."
python manage.py migrate || { echo "ERROR: Django migration failed"; exit 1; }

echo "==> Collecting static files..."
python manage.py collectstatic --no-input || { echo "ERROR: Django collectstatic failed"; exit 1; }

# Execute the main command (passed as arguments)
echo "==> Executing startup command: $@"
exec "$@"
