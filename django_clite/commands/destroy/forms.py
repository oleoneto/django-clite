import click

from pathlib import Path
from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import RemoveLineFromFile
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands.callbacks import sanitized_string_callback
from django_clite.commands import command_defaults


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def form(ctx, name):
    """
    Destroy a form.
    """

    File(name=f"forms/{name}.py").destroy(
        after_hooks=[
            RemoveLineFromFile(Path("forms/__init__.py"), command_defaults.form(name)),
        ],
        **ctx.obj,
    )
