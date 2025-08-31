web: cd backend && python3 manage.py migrate && python3 manage.py create_timeslots && gunicorn --bind 0.0.0.0:$PORT my_timetable.wsgi:application
release: cd backend && python manage.py collectstatic --noinput
