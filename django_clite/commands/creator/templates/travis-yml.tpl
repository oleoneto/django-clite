language: python
python:
  - "3.7"
env:
  - DJANGO_VERSION=2.2.3
branches:
  only:
    - master
# Start services.
services:
  - redis-server
  - postgresql
# command to install dependencies
install:
  - pip install -q Django==$DJANGO_VERSION
  - pip install -r requirements/local.txt
  - pip install coveralls
before_script:
  - psql -c "CREATE DATABASE db;" -U postgres
  - cp .env.example .env
  - python manage.py migrate
  - python manage.py collectstatic --noinput
# command to run tests
script:
  - pytest
after_success:
  - coveralls
