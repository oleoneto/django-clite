import click

from pathlib import Path
from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import RemoveLineFromFile
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def signal(ctx, name):
    """
    Destroy a signal.
    """

    File(name=f"models/signals/{name}.py").destroy(
        after_hooks=[
            RemoveLineFromFile(
                Path(f"models/signals/__init__.py"),
                command_defaults.signal(name)
            ),
        ],
        **ctx.obj
    )
