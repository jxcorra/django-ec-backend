!#/usr/bin/bash

echo "Running migrations"
./manage.py migrate

echo "Uploading test data"
./manage.py uploadcarmodels --with-reset --max-workers=2

echo "Starting gunicorn"
gunicorn easycar.wsgi \
        --bind 0.0.0.0:5000 \
        --reload \
        --max-requests 100 \
        --threads 2 \
        --access-logfile -