import click

from geny.core.filesystem.files import File
from cli.commands.callbacks import sanitized_string_callback
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def manager(ctx, name):
    """
    Destroy a model manager.
    """

    File(name=f"models/managers/{name}.py").create(**ctx.obj)
