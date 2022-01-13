import click
from cli.commands.generate.helpers import resource_generator


@click.command()
@click.argument("name", required=True)
@click.pass_context
def manager(ctx, name):
    """
    Generates a model manager under the model managers' directory.
    """

    resource_generator(name, template='manager.tpl', parent='models', package='managers', **ctx.obj)
