import inflection
import click
from cli.commands.generate.helpers import resource_generator
from cli.utils.fs.utils import change_directory
from cli.handlers.filesystem.directory import Directory
from cli.handlers.filesystem.template_handler import TestTemplateHandler


@click.command()
@click.argument("name", required=True)
@click.option("-s", "--scope", type=click.Choice(['model', 'viewset']), required=True)
@click.pass_context
def test(ctx, name, scope):
    """
    Generates a new TestCase.
    """

    parent = 'tests'

    Directory.ensure_directory(parent)

    change_directory(parent)

    resource_generator(
        name,
        template=f"{inflection.singularize(scope)}.tpl",
        package=inflection.pluralize(scope),
        scope='TestCase',
        template_handler=TestTemplateHandler,
        **ctx.obj,
    )
