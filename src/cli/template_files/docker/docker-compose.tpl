version: '3'

{% if 'database' in services %}
volumes:
    database:
{% endif %}

services:
  app:
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
    command: "gunicorn {{ project }}.wsgi:application --bind 0.0.0.0:{{ port }} --workers {{ workers }}"
    ports:
        - 8007:8000 # host:docker
    {%- if services %}
    depends_on:
        {%- for service in services %}
        - {{ service }}
        {% endfor %}
    {% endif %}


  {%- if 'database' in services %}
  database:
    container_name: "{{ project }}_database"
    image: postgres:12-alpine
    labels:
        com.database.description: "{{ project }}: Database service"
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
  {% endif %}

  {%- if 'redis' in services %}
  redis:
    container_name: "{{ project }}_redis"
    image: redis:latest
    labels:
        com.redis.description: "{{ project }}: Redis cache service"
    ports:
        - 6377:6379 # host:docker
    restart: always
  {% endif %}

  {%- if 'celery' in services %}
  celery_worker:
    container_name: "{{ project }}_celery_worker"
    labels:
        com.celery.description: "{{ project }}: Celery Worker"
    build:
      context: .
    command: celery worker --app {{ project }} --concurrency=20 -linfo -E
    depends_on:
      - redis
    env_file:
      - .env
    restart: on-failure
    stop_grace_period: 5s
  {% endif %}


# These settings are provided for development purposes only. Not suitable for production.