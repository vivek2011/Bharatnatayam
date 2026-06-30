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
python manage.py migrate
python manage.py collectstatic --no-input

# Execute the main command (passed as arguments)
exec "$@"
