import click

from cli.commands.callbacks import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope
from cli.commands import command_defaults


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def signal(ctx, name):
    """
    Destroy a signal.
    """

    File(name=f"models/signals/{name}.py").destroy(**{
        "import_statement": command_defaults.signal(name),
        **ctx.obj,
    })
