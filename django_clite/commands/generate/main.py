# cli:commands:generate
import click

from django_clite.commands.generate.admin import admin, admin_inline as admin_inline
from django_clite.commands.generate.dockerfile import dockerfile
from django_clite.commands.generate.fixtures import fixture
from django_clite.commands.generate.forms import form
from django_clite.commands.generate.management import management
from django_clite.commands.generate.managers import manager
from django_clite.commands.generate.models import model, scaffold
from django_clite.commands.generate.serializers import serializer
from django_clite.commands.generate.signals import signal
from django_clite.commands.generate.tags import tag
from django_clite.commands.generate.template import template
from django_clite.commands.generate.tests import test
from django_clite.commands.generate.validators import validator
from django_clite.commands.generate.views import view
from django_clite.commands.generate.viewsets import viewset


@click.group()
@click.option("--project", type=click.Path(), help="Project name.")
@click.option("--app", type=click.Path(), help="Application name.")
@click.pass_context
def generate(ctx, project, app):
    """
    Create application resources.
    """

    ctx.ensure_object(dict)


[
    generate.add_command(cmd)
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
