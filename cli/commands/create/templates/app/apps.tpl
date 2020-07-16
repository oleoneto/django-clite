from django.apps import AppConfig


class {{ app.capitalize() }}Config(AppConfig):
    name = '{{ project }}.{{ app }}'

    def ready(self):
        from .models import signals
