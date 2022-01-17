import click
from cli.utils import inside_app_directory
from cli.commands.destroy.admin import admin
from cli.commands.destroy.fixture import fixture
from cli.commands.destroy.form import form
from cli.commands.destroy.manager import manager
from cli.commands.destroy.resource import model, resource
from cli.commands.destroy.serializer import serializer
from cli.commands.destroy.signal import signal
from cli.commands.destroy.template import template, templatetag
from cli.commands.destroy.test import test
from cli.commands.destroy.validator import validator
from cli.commands.destroy.view import view
from cli.commands.destroy.viewset import viewset


@click.group()
@click.pass_context
def destroy(ctx):
    """
    Removes models, forms, views, and other resources
    """

    ctx.ensure_object(dict)

    if not inside_app_directory(ctx, exit_on_error=not ctx.obj['force']):
        click.Abort()


subcommands = [
    admin,
    fixture,
    form,
    manager,
    model,
    resource,
    serializer,
    signal,
    template,
    templatetag,
    test,
    validator,
    view,
    viewset,
]

for command in subcommands:
    destroy.add_command(command)
