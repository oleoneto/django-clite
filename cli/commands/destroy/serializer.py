import click
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer


@click.command()
@click.argument('name', required=True)
@click.pass_context
def serializer(ctx, name):
    """
    Destroys a serializer.
    """

    resource_destroyer(name, package='serializers', **ctx.obj)
