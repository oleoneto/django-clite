import click
import inflection
from cli.commands.generate.helpers import resource_generator


@click.command()
@click.argument("name", required=True)
@click.pass_context
def signal(ctx, name):
    """
    Generates a signal.
    """

    resource_generator(
        name,
        template='signal.tpl',
        parent='models',
        package='signals',
        import_context={'classname': f"{inflection.underscore(name)}"},
        **ctx.obj
    )
