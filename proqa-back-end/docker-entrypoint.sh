#!/bin/bash

if [[ -z "${CELERY+x}" ]]; then
  echo "Not Celery, continuing"
else
  if [[ -z "${DEV}" ]]; then
    celery -A proqa_back_end worker -l INFO
  else
    watchfiles --filter python 'celery -A proqa_back_end worker -l INFO' api proqa_back_end
  fi
  exit 0
fi

if [[ -z "${FIRST+x}" ]]; then
  echo "Not first run, continuing"
else
  python manage.py migrate
  python manage.py loaddata tests/api/resources/dummy_data.json
  exit 0
fi

if [[ -z "${DEV}" ]]; then
  echo "Running in prod mode!"
  python manage.py collectstatic --noinput
  gunicorn -t $TIMEOUT --bind 0.0.0.0:8000 proqa_back_end.wsgi:application
else
  echo "Running in dev mode!"
  python manage.py migrate
  python manage.py loaddata tests/api/resources/dummy_data.json
  python manage.py runserver 0.0.0.0:8000
fi
