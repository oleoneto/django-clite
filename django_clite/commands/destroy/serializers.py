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
def serializer(ctx, name):
    """
    Destroy a serializer for a given model.
    """

    File(name=f"serializers/{name}.py").destroy(
        after_hooks=[
            RemoveLineFromFile(
                Path(f"serializers/__init__.py"),
                command_defaults.serializer(name)
            ),
        ],
        **ctx.obj
    )
