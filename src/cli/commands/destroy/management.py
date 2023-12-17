import click

from cli.utils import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command(name="command")
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def management(ctx, name):
    """
    Destroy an application command.
    """

    File(name=f"management/{name}.py").destroy(**ctx.obj)
