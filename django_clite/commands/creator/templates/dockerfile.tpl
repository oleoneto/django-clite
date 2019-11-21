FROM python:3.6.5

# Environment variables
ENV PYTHONUNBUFFERED 1
RUN apt-get update

# Install some necessary dependencies.
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

RUN pip install -U pip
ADD requirements.txt /code/
RUN pip install -Ur /code/requirements.txt

# Set working directory
WORKDIR /code/

# Copy requirements to working directory
COPY ./requirements.txt .

# Copy project files
COPY . /code/
