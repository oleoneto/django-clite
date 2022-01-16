import click
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer


@click.command()
@click.argument('name', required=True)
@click.option('--inline', is_flag=True, help='Destroy inline admin model')
@click.pass_context
def admin(ctx, name, inline):
    """
    Destroys an admin model.
    """

    if inline:
        resource_destroyer(name, parent='admin', package='inlines', **ctx.obj)
    else:
        resource_destroyer(name, package='admin', **ctx.obj)
