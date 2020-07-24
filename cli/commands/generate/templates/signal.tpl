from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.template import Context
from django.db.models.signals import pre_save, post_save, post_delete
# from ..models import MyModel
# from ...tasks import my_task


# template = get_template('template.txt')


# @receiver(post_save, sender=MyModel, dispatch_uid="{{ name }}")
def {{ model }}(sender, **kwargs):
    instance = kwargs.get('instance')
    # code here...
