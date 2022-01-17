import click
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer


@click.command()
@click.argument('name', required=True)
@click.pass_context
def manager(ctx, name):
    """
    Destroys a model manager.
    """

    resource_destroyer(name, parent='models', package='managers', **ctx.obj)
