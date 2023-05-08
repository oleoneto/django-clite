# cli:commands:generate
import click
from cli.commands.generate.admin import admin, inline as admin_inline
from cli.commands.generate.fixtures import fixture
from cli.commands.generate.forms import form
from cli.commands.generate.managers import manager
from cli.commands.generate.models import model
from cli.commands.generate.serializers import serializer
from cli.commands.generate.tags import tag
from cli.commands.generate.template import template
from cli.commands.generate.tests import test
from cli.commands.generate.validators import validator


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


[
    generate.add_command(command)
    for command in [
        admin,
        admin_inline,
        fixture,
        form,
        manager,
        model,
        serializer,
        tag,
        template,
        test,
        validator,
    ]
]
