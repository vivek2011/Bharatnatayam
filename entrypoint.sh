#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

# Run migrations and collect static files
python manage.py migrate
python manage.py collectstatic --no-input

# Execute the main command (passed as arguments)
exec "$@"
