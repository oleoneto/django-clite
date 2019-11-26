FROM python:3.6

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update

# Install some necessary dependencies.
RUN apt-get install -y swig libssl-dev dpkg-dev netcat gunicorn

RUN pip install -U pip gunicorn
RUN pip install pipenv

# Create working directory
RUN mkdir /code

# Copy requirements to working directory
ADD Pipfile /code/Pipfile
ADD Pipfile.lock /code/Pipfile.lock

# Set working directory
WORKDIR /code

# Install dependencies
RUN pipenv lock -r | cat > /code/requirements.txt
RUN pipenv install --deploy
RUN pip install -r requirements.txt

# Copy project files
COPY . /code/
