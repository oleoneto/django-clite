import click

from geny.core.filesystem.files import File
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands.callbacks import sanitized_string_callback


@scoped(to=Scope.APP)
@click.command(name="command")
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def management(ctx, name):
    """
    Destroy an application command.
    """

    File(name=f"management/{name}.py").destroy(**ctx.obj)
