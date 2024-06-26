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
    Generate an application command.
    """

    file = File(
        name=f"management/{name}.py",
        template="management.tpl",
        context={
            "name": name,
        },
    )

    file.create(**ctx.obj)
