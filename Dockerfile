# Base image
FROM python:3.13.0a4-alpine

LABEL MAINTAINER="Leo Neto"

# Working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Copy other files to docker container
COPY . .

# Install dependencies
RUN apk add gcc musl-dev linux-headers && pip install -e .

CMD ["django-clite"]
