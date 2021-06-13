!#/usr/bin/bash

echo "Running migrations"
./manage.py migrate

echo "Starting gunicorn"
gunicorn easycar.wsgi \
        --bind 0.0.0.0:8000 \
        --reload \
        --max-requests 100 \
        --threads 2 \
        --access-logfile -