import click

from pathlib import Path
from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import RemoveLineFromFile
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands.callbacks import sanitized_string_callback
from django_clite.commands import command_defaults


@scoped(to=Scope.APP)
@click.command(name="command")
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def management(ctx, name):
    """
    Destroy an application command.
    """

    File(name=f"management/{name}.py").destroy(**ctx.obj)

    File(name=f"admin/inlines/{name}.py").destroy(
        after_hooks=[
            RemoveLineFromFile(
                Path("admin/inlines/__init__.py"), command_defaults.admin(name)
            ),
        ],
        **ctx.obj,
    )
