version: '3'

services:
  web:
    container_name: "{{ project }}-web"
    labels:
        com.{{ project }}.web.description = "{{ project }}: Web Application"
    build: ./
    command: gunicorn {{ project }}.wsgi:application --bind 0.0.0.0:8000 --workers 3
    ports:
        - "8093:8000" # host:docker
    networks:
        - {{ project }}_network
    env_file:
        - .env
    depends_on:
        - db


  db:
    image: postgres:10.5-alpine
    labels:
        com.{{ project }}.db.description: "{{ project }}: Database service"
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
        - {{ project }}_network
    healthcheck:
      test: ["CMD-SHELL", "pg_ready -U postgres"]
      interval: 10s
      timeout: 83s
      retries: 40
    restart: always


  nginx:
    container_name: "{{ project }}-nginx"
    labels:
        com.{{ project }}.nginx.description: "{{ project }}: Proxy Server"
    image: nginx:1.15.0-alpine
    ports:
      - 1337:80 # host:docker
    depends_on:
      - web


  redis:
    restart: always
    image: redis:latest
    expose:
      - "6379"


networks:
  {{ project }}_network:
    driver: bridge


volumes:
  postgres_data:
