# {{ project }}:{{ app }}:audit
"""
If you haven't already,
install django-auditlog and add it to your project's INSTALLED_APPS
"""
from auditlog.registry import auditlog
from {{ project }}.{{ app }} import models

# register models for auditing...
# auditlog.register(models.MyModel)
