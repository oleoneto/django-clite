import click
from cli.commands.generate.helpers import resource_generator
from cli.utils.fs.utils import change_directory
from cli.handlers.filesystem import Directory


@click.command()
@click.argument("name", required=True)
@click.pass_context
def manager(ctx, name):
    """
    Generates a model manager under the model managers' directory.
    """

    parent = 'models'

    Directory.ensure_directory(parent)

    change_directory(parent)

    resource_generator(name, template='manager.tpl', package='managers', **ctx.obj)
