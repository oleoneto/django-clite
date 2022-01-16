import click
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer


@click.command()
@click.argument("name", required=True)
@click.pass_context
def validator(ctx, name):
    """
    Generates a validator.
    """

    resource_destroyer(
        name,
        parent='models',
        package='validators',
        import_template="""from .{{ module }} import {{ module }}""",
        **ctx.obj
    )
