FROM python:3.7

# Environment variables
ENV PYTHONUNBUFFERED 1
RUN apt-get update

# Install some necessary dependencies.
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

RUN pip install -U pip
RUN pip install pipenv

# Copy requirements to working directory
ADD Pipfile* /code/

# Set working directory
WORKDIR /code/

# Install dependencies
RUN pipenv install --deploy

# Copy project files
COPY . /code/
