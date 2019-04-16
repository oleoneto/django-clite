from jinja2 import Template


dockerfile = Template("""FROM python:3.6.5

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
""")


docker_compose = Template("""version: '3'

services:
  web:
    container_name: "{{ project.lower() }}-web"
    labels:
        com.{{ project.lower() }}.web.description = "Web Application"
    build: ./application
    volumes:
        - ./application/:code/
        - static_volume:/var/www/staticfiles
        - media_volume:/var/www/mediafiles
    ports:
        - "8093:8000"
    networks:
        - {{ project }}_network 
    env_file:
        - .env
    depends_on:
        - db
    command: gunicorn {{ project }}.wsgi:application --bind 0.0.0.0:8000 --workers 3
  
  
  db:
    image: postgres:10.5-alpine
    labels:
        com.{{ project.lower() }}.db.description: "Database service"
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
        - {{ project.lower() }}_network
    restart: always
  
  nginx:
    container_name: "{{ project.lower() }}-nginx"
    labels:
        com.{{ project.lower() }}.nginx.description: "Proxy Server"
    image: nginx:1.15.0-alpine
    volumes:
      - static_volume:/var/www/staticfiles
      - media_volume:/var/www/mediafiles
    ports:
      - 1337:80
    depends_on:
      - web
      
volumes:
  postgres_data:
  static_volume:
  media_volume:
""")
