# cli:commands:destroy
import click

from cli.commands.destroy.admin import admin, admin_inline as admin_inline
from cli.commands.destroy.fixtures import fixture
from cli.commands.destroy.forms import form
from cli.commands.destroy.management import management
from cli.commands.destroy.managers import manager
from cli.commands.destroy.models import model, scaffold
from cli.commands.destroy.serializers import serializer
from cli.commands.destroy.signals import signal
from cli.commands.destroy.tags import tag
from cli.commands.destroy.template import template
from cli.commands.destroy.tests import test
from cli.commands.destroy.validators import validator
from cli.commands.destroy.views import view
from cli.commands.destroy.viewsets import viewset


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
