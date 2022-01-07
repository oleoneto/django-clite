import os
import click
from cli.utils.fs.utils import inside_app_directory
from cli.handlers.filesystem import FileHandler
from cli.commands.generate.admin import admin
from cli.commands.generate.fixture import fixture
from cli.commands.generate.form import form
from cli.commands.generate.manager import manager
# from cli.commands.generate.resource import model, resource, search_index
from cli.commands.generate.serializer import serializer
from cli.commands.generate.signal import signal
from cli.commands.generate.template import template, templatetag
from cli.commands.generate.test import test
from cli.commands.generate.validator import validator
from cli.commands.generate.view import view
from cli.commands.generate.viewset import viewset


@click.group()
@click.option('--directory', '-d', type=click.Path(), help="Specify path to your project's management file.")
@click.pass_context
def generate(ctx, directory):
    """
    Adds models, routes, and other resources
    """
    ctx.ensure_object(dict)

    ctx.obj['scoped_context'] = {
        'verbose': ctx.obj['verbose'],
        'force': ctx.obj['force'],
        'dry': ctx.obj['dry'],
    }

    ctx.obj['project_files'] = FileHandler.find_files(
        path=directory or os.getcwd(),
        patterns=['apps.py']
    )

    if not inside_app_directory(ctx, exit_on_error=not ctx.obj['force']):
        raise click.Abort


subcommands = [
    admin,
    fixture,
    form,
    manager,
    # model,
    # resource,
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
    generate.add_command(command)
