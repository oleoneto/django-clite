# django_clite:commands:destroy
import click

from django_clite.commands.destroy.admin import admin, admin_inline as admin_inline
from django_clite.commands.destroy.dockerfile import dockerfile
from django_clite.commands.destroy.fixtures import fixture
from django_clite.commands.destroy.forms import form
from django_clite.commands.destroy.management import management
from django_clite.commands.destroy.managers import manager
from django_clite.commands.destroy.models import model, scaffold
from django_clite.commands.destroy.serializers import serializer
from django_clite.commands.destroy.signals import signal
from django_clite.commands.destroy.tags import tag
from django_clite.commands.destroy.template import template
from django_clite.commands.destroy.tests import test
from django_clite.commands.destroy.validators import validator
from django_clite.commands.destroy.views import view
from django_clite.commands.destroy.viewsets import viewset


@click.group()
@click.pass_context
def destroy(ctx):
    """
    Destroy application resources.
    """

    ctx.ensure_object(dict)


[
    destroy.add_command(cmd)
    for cmd in [
        admin,
        admin_inline,
        dockerfile,
        fixture,
        form,
        management,
        manager,
        model,
        scaffold,
        serializer,
        signal,
        tag,
        template,
        test,
        validator,
        view,
        viewset,
    ]
]
