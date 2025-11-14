#!/bin/bash
set -e

cd backend

# Collect static files (non-blocking)
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=my_timetable.settings_render || echo "Warning: Static files collection failed, continuing..."

# Try to run migrations (non-blocking - app will start even if this fails)
echo "Running migrations..."
timeout 30 python manage.py migrate --settings=my_timetable.settings_render || {
    echo "Warning: Migrations failed or timed out. App will start anyway."
    echo "Database may not be ready yet or DATABASE_URL may be incorrect."
    echo "Please check:"
    echo "1. Database is created and running in Render"
    echo "2. Database is linked to this web service"
    echo "3. DATABASE_URL environment variable is set"
}

# Start gunicorn
echo "Starting gunicorn..."
exec gunicorn my_timetable.wsgi:application --bind 0.0.0.0:$PORT

