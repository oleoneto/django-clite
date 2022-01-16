import click
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer


@click.command()
@click.argument('name', required=True)
@click.pass_context
def signal(ctx, name):
    """
    Destroys a signal.
    """

    resource_destroyer(
        name,
        parent='models',
        package='signals',
        import_template="""from .{{module}} import {{module}}""",
        **ctx.obj
    )
