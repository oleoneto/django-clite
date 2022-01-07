import click
from cli.commands.generate.helpers import resource_generator


@click.command()
@click.option('-r', '--read-only', is_flag=True, help="Create a read-only viewset.")
@click.argument("name", required=True)
@click.pass_context
def viewset(ctx, read_only, name):
    """
    Generates a viewset for a serializable model.
    """

    resource_generator(
        name,
        template='viewset.tpl',
        package='viewsets',
        context={'read_only': read_only},
        **ctx.obj
    )
