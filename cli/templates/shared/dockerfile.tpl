# Base image
FROM python:3.7-slim-stretch

# Working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Copy dependencies
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Install dependencies
RUN apt-get update \
    && apt-get install -y \
    swig libssl-dev dpkg-dev \
    && pip install -U pip pipenv gunicorn Faker \
    && pipenv lock --requirements > requirements.txt \
    && pip install -r requirements.txt \
    && chmod +x /docker-entrypoint.sh


# Copy other files to docker container
COPY . .

# Switch users
RUN groupadd -r docker && useradd --no-log-init -r -g docker docker
USER docker

CMD ["python3", "manage.py", "runserver"]
