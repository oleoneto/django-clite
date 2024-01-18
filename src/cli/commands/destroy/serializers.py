import click

from geny.core.filesystem.files import File
from cli.commands.callbacks import sanitized_string_callback
from cli.decorators.scope import scoped, Scope
from cli.commands import command_defaults


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def serializer(ctx, name):
    """
    Destroy a serializer for a given model.
    """

    File(name=f"serializers/{name}.py").destroy(
        **{
            "import_statement": command_defaults.serializer(name),
            **ctx.obj,
        }
    )
