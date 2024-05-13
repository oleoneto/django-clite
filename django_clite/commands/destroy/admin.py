import click

from pathlib import Path
from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import RemoveLineFromFile
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.pass_context
def admin(ctx, name):
    """
    Destroy an admin model.
    """

    File(name=f"admin/{name}.py").destroy(
        after_hooks=[
            RemoveLineFromFile(Path("admin/__init__.py"), command_defaults.admin(name)),
        ],
        **ctx.obj,
    )


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.pass_context
def admin_inline(ctx, name):
    """
    Destroy an inline admin model.
    """

    File(name=f"admin/inlines/{name}.py").destroy(
        after_hooks=[
            RemoveLineFromFile(
                Path("admin/inlines/__init__.py"), command_defaults.admin_inline(name)
            ),
        ],
        **ctx.obj,
    )
