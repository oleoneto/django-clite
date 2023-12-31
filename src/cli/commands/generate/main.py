# cli:commands:generate
import click

from cli.commands.generate.admin import admin, admin_inline as admin_inline
from cli.commands.generate.fixtures import fixture
from cli.commands.generate.forms import form
from cli.commands.generate.management import management
from cli.commands.generate.managers import manager
from cli.commands.generate.models import model, scaffold
from cli.commands.generate.serializers import serializer
from cli.commands.generate.signals import signal
from cli.commands.generate.tags import tag
from cli.commands.generate.template import template
from cli.commands.generate.tests import test
from cli.commands.generate.validators import validator
from cli.commands.generate.views import view
from cli.commands.generate.viewsets import viewset


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
