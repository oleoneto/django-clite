# cli:commands:generate
import click
from cli.commands.generate.admin import admin, admin_inline as admin_inline
from cli.commands.generate.fixtures import fixture
from cli.commands.generate.forms import form
from cli.commands.generate.management import management
from cli.commands.generate.managers import manager
from cli.commands.generate.models import model
from cli.commands.generate.serializers import serializer
from cli.commands.generate.signals import signal
from cli.commands.generate.tags import tag
from cli.commands.generate.template import template
from cli.commands.generate.tests import test
from cli.commands.generate.validators import validator
from cli.constants import DJANGO_FILES_KEY
from cli.core.filesystem import FileSystem


@click.group()
@click.option(
    "--directory",
    "-d",
    type=click.Path(),
    help="Specify the path to the project's management file.",
)
@click.pass_context
def generate(ctx, directory):
    """
    Create application resources.
    """

    ctx.ensure_object(dict)

    if len(ctx.obj[DJANGO_FILES_KEY]) == 0 and not FileSystem().force:
        click.echo("Django project not detected")
        raise click.Abort


[
    generate.add_command(command)
    for command in [
        admin,
        admin_inline,
        fixture,
        form,
        management,
        manager,
        model,
        serializer,
        signal,
        tag,
        template,
        test,
        validator,
    ]
]
