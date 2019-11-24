image: python:3.7.2
pipelines: 
  default: 
    - step:
        script:
          - pip install django
          - python manage.py test
      services: 
        - postgres 
        - redis
definitions: 
  services: 
    postgres: 
      image: postgres
    redis:
      image: redis
