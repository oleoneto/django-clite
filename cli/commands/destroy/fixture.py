import click
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer


@click.command()
@click.argument('name')
@click.pass_context
def fixture(ctx, name):
    """
    Destroys a fixture.
    """

    resource_destroyer(name, package='fixtures', file_extension='.json', **ctx.obj)
