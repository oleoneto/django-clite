from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.template import Context
from django.db.models.signals import pre_save, post_save, post_delete
{%- if related_model %}
from ..models import {{ related_model }}
{% else %}
# from ..models import MyModel
{%- endif %}


# template = get_template('template.txt')


# @receiver(post_save, sender={% if related_model %}{{ related_model }}{% else %}MyModel{% endif %}, dispatch_uid="{{ name }}")
def {{ name }}(sender, **kwargs):
    instance = kwargs.get('instance')
    # code here...
