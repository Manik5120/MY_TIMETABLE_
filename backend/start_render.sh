#!/bin/bash
# Don't use set -e so we can handle errors gracefully

cd backend

# Collect static files (non-blocking)
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=my_timetable.settings_render || echo "Warning: Static files collection failed, continuing..."

# Try to run migrations (non-blocking - app will start even if this fails)
echo "Running migrations..."
python manage.py migrate --settings=my_timetable.settings_render 2>&1 || {
    echo "Warning: Migrations failed. App will start anyway."
    echo "This is OK if using SQLite or if database is not yet configured."
}

# Start gunicorn
echo "Starting gunicorn..."
exec gunicorn my_timetable.wsgi:application --bind 0.0.0.0:$PORT

