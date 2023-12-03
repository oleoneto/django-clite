#!/bin/bash

# Collect staticfiles
python3 manage.py collectstatic --noinput

# Apply database migrations
python3 manage.py migrate

# Seed database
# python3 manage.py loaddata /path/to/fixtures

exec "$@"
