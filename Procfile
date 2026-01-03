web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn IntelliFace.wsgi:application --bind 0.0.0.0:$PORT
