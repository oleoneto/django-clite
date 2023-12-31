import click
import inflection

from cli.commands.callbacks import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope
from cli.commands import command_defaults


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def serializer(ctx, name, skip_import):
    """
    Generate a serializer for a given model.

    Checks for the existence of the specified model in models.py
    before attempting to create a serializer for it. Aborts if model is not found.
    """

    file = File(
        name=f"serializers/{name}.py",
        template="serializer.tpl",
        context={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )

    file.create(
        import_statement=command_defaults.serializer(name),
        add_import_statement=not skip_import,
        **ctx.obj,
    )
