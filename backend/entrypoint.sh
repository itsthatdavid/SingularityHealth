#!/bin/sh

# Wait for database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "PostgreSQL is ready!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

# Load initial data if needed
echo "Loading initial data..."
python manage.py loaddata initial_data.json || true

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000