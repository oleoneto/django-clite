version: '3'

services:
  web:
    container_name: "{{ project }}_web"
    labels:
        com.{{ project }}.web.description: "{{ project }}: Web Application"
    build:
        context: .
    volumes:
        - .:/app
    env_file:
        - .env
    environment:
        DJANGO_ENV: docker
    entrypoint: /docker-entrypoint.sh
    command: gunicorn {{ project }}.wsgi:application --bind 0.0.0.0:8000 --workers 3
    ports:
        - 8007:8000 # host:docker
    depends_on:
        - db
        - redis


  db:
    container_name: "{{ project }}_db"
    image: postgres:12-alpine
    labels:
        com.{{ project }}.db.description: "{{ project }}: Database service"
    volumes:
        - ./database:/var/lib/postgresql/data/
    ports:
        - 5437:5432 # host:docker
    healthcheck:
        test: ["CMD-SHELL", "pg_ready -U postgres"]
        interval: 10s
        timeout: 83s
        retries: 40
    restart: always


  redis:
    container_name: "{{ project }}_redis"
    image: redis:latest
    labels:
        com.{{ project }}.redis.description: "{{ project }}: Redis cache service"
    ports:
        - 6377:6379 # host:docker
    restart: always


volumes:
    database:
