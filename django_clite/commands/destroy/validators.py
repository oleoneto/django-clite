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
def validator(ctx, name):
    """
    Destroy a validator.
    """

    File(name=f"models/validators/{name}.py").destroy(
        after_hooks=[
            RemoveLineFromFile(
                Path("models/validators/__init__.py"), command_defaults.validator(name)
            ),
        ],
        **ctx.obj,
    )
