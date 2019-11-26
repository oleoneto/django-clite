from django.apps import AppConfig


class {{ app.capitalize() }}Config(AppConfig):
    name = '{{ project }}.{{ app }}'
