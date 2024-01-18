import click

from geny.core.filesystem.files import File
from cli.commands.callbacks import sanitized_string_callback
from cli.decorators.scope import scoped, Scope
from cli.commands import command_defaults


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def validator(ctx, name):
    """
    Destroy a validator.
    """

    File(name=f"models/validators/{name}.py").destroy(
        **{
            "import_statement": command_defaults.validator(name),
            **ctx.obj,
        }
    )
