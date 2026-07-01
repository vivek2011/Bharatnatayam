#!/bin/sh

# Determine DB host/port from either explicit vars or DATABASE_URL
if [ -n "$SQL_HOST" ] && [ -n "$SQL_PORT" ]; then
    DB_HOST="$SQL_HOST"
    DB_PORT="$SQL_PORT"
elif [ -n "$DATABASE_URL" ]; then
    # Use Python's urlparse to reliably extract host and port (handles missing port)
    DB_HOST=$(python3 -c "from urllib.parse import urlparse; u=urlparse('$DATABASE_URL'); print(u.hostname)")
    DB_PORT=$(python3 -c "from urllib.parse import urlparse; u=urlparse('$DATABASE_URL'); print(u.port or 5432)")
fi

if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
    echo "Waiting for postgres ($DB_HOST:$DB_PORT)..."
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        sleep 0.1
    done
    echo "PostgreSQL started"
else
    echo "No DB host/port found (SQL_HOST/SQL_PORT or DATABASE_URL). Skipping wait."
fi

# Run migrations and collect static files
echo "==> Running Django database migrations..."
python manage.py migrate || { echo "ERROR: Django migration failed"; exit 1; }

echo "==> Collecting static files..."
python manage.py collectstatic --no-input || { echo "ERROR: Django collectstatic failed"; exit 1; }

# Execute the main command (passed as arguments)
echo "==> Executing startup command: $@"
exec "$@"
