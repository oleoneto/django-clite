import click

from cli.utils import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.pass_context
def admin(ctx, name):
    """
    Destroy an admin model.
    """

    File(name=f"admin/{name}.py").destroy(**ctx.obj)


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.pass_context
def admin_inline(ctx, name):
    """
    Destroy an inline admin model.
    """

    File(name=f"admin/inlines/{name}.py").destroy(**ctx.obj)
