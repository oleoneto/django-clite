import click
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer


@click.command()
@click.argument('name', required=True)
@click.pass_context
def viewset(ctx, name):
    """
    Destroys a viewset.
    """

    resource_destroyer(name, package='viewsets', **ctx.obj)
