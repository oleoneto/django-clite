import click
from cli.commands.generate.helpers import resource_generator


@click.command()
@click.argument("name", required=True)
@click.pass_context
def validator(ctx, name):
    """
    Generates a validator.
    """

    resource_generator(
        name,
        template='validator.tpl',
        parent='models',
        package='validators',
        import_template="""from .{{ module }} import {{ module }}""",
        **ctx.obj
    )
