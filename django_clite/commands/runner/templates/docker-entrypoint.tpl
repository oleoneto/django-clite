#!/bin/bash

if [ "$DJANGO_ENV" = "docker" ]; then
  # Collect staticfiles
   python3 manage.py collectstatic --noinput
fi

# Apply database migrations
python3 manage.py migrate

exec "$@"
