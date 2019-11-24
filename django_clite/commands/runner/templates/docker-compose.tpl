version: '3'

services:
  web:
    container_name: "{{ project }}-web"
    labels:
        com.{{ project }}.web.description = "{{ project }}: Web Application"
    build: ./application
    volumes:
        - ./application/:code/
        - static_volume:/var/www/static
        - media_volume:/var/www/media
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
        com.{{ project }}.db.description: "{{ project }}: Database service"
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
        - {{ project }}_network
    restart: always


  nginx:
    container_name: "{{ project }}-nginx"
    labels:
        com.{{ project }}.nginx.description: "{{ project }}: Proxy Server"
    image: nginx:1.15.0-alpine
    volumes:
      - static_volume:/var/www/static
      - media_volume:/var/www/media
    ports:
      - 1337:80
    depends_on:
      - web


  redis:
    restart: always
    image: redis:latest
    expose:
      - "6379"

volumes:
  postgres_data:
  static_volume:
  media_volume:
