from django.apps import AppConfig


class {{ app.capitalize() }}Config(AppConfig):
    name = '{% if project %}{{ project }}.{% endif %}{{ app }}'

    def ready(self):
        from .models import signals
