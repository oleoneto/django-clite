from django.apps import AppConfig


class {{ app.capitalize() }}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{% if project %}{{ project }}.{% endif %}{{ app }}'

    def ready(self):
        from .models import signals
