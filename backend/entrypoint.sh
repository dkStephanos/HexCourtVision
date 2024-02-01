#!/bin/sh

# Wait for database to be ready
# Perform any other necessary checks
until PGPASSWORD=$DATABASE_PASSWORD psql -h "db" -p "5432" -U "$DATABASE_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Apply migrations
python ./backend/manage.py makemigrations
python ./backend/manage.py migrate

# Start the Django application
exec python ./backend/manage.py runserver 0.0.0.0:8000
