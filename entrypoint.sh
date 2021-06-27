!#/bin/bash

echo "Running migrations"
./manage.py migrate

function start_backend() {
  echo "Uploading test data"
  ./manage.py uploadcarmodels --with-reset --max-workers=2

  echo "Starting gunicorn"
  gunicorn easycar.wsgi \
          --bind 0.0.0.0:5000 \
          --reload \
          --max-requests 100 \
          --threads 2 \
          --access-logfile -
}

function start_worker() {
    celery --app=eccelery worker \
           -l DEBUG -c 2 \
           -Q "$QUEUES"
}

function start_beat() {
    celery --app=eccelery beat -l DEBUG
}

case $SERVICE in
backend)
  start_backend
  ;;
worker)
  start_worker
  ;;
beat)
  start_beat
  ;;
esac
