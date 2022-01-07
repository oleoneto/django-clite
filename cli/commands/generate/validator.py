import click
from cli.commands.generate.helpers import resource_generator
from cli.utils.fs.utils import change_directory
from cli.handlers.filesystem import Directory


@click.command()
@click.argument("name", required=True)
@click.pass_context
def validator(ctx, name):
    """
    Generates a validator.
    """

    parent = 'models'

    Directory.ensure_directory(parent)

    change_directory(parent)

    resource_generator(
        name,
        template='validator.tpl',
        package='validators',
        import_template="""from .{{ module }} import {{ module }}""",
        **ctx.obj
    )
