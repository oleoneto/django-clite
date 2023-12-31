import click

from cli.commands.callbacks import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope
from cli.commands import command_defaults


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def tag(ctx, name):
    """
    Generate a template tag.
    """

    File(name=f"templatetags/{name}.py").destroy(
        **{
            "import_statement": command_defaults.tag(name),
            **ctx.obj,
        }
    )
