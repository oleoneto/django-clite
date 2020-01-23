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
COPY requirements.txt .requirements
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Install dependencies
RUN apt-get update \
    && apt-get install -y \
    swig libssl-dev dpkg-dev \
    && pip install -U pip gunicorn Faker \
    && pip install -r .requirements \
    && chmod +x /docker-entrypoint.sh


# Copy other files to docker container
COPY . .


CMD ["python3", "manage.py", "runserver"]
