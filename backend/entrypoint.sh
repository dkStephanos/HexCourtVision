#!/bin/sh

# Wait for database to be ready
# Perform any other necessary checks
until PGPASSWORD=$DATABASE_PASSWORD psql -h "db" -p "5432" -U "$DATABASE_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Apply migrations
python ./manage.py makemigrations
python ./manage.py migrate

# Start the Django application
exec python ./manage.py runserver 0.0.0.0:8000 &

# Start Jupyter Notebook using django-extensions shell_plus
python ./manage.py shell_plus --notebook
