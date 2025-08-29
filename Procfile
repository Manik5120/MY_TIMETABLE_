web: cd backend && python manage.py migrate && python manage.py create_timeslots && gunicorn my_timetable.wsgi:application --bind 0.0.0.0:$PORT
release: cd backend && python manage.py collectstatic --noinput
