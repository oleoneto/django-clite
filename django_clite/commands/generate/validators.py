import click
import pathlib

from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import AddLineToFile, TouchFile
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback


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
def validator(ctx, name, skip_import):
    """
    Generate a validator.
    """

    file = File(
        name=f"models/validators/{name}.py",
        template="models/validator.tpl",
        context={
            "name": name,
        },
    )

    after_hooks = [
        TouchFile('models/validators/__init__.py')
    ]

    if not skip_import:
        after_hooks.append(
            AddLineToFile(
                pathlib.Path('models/validators/__init__.py'),
                command_defaults.validator(name),
                prevent_duplicates=True,
            )
        )

    file.create(after_hooks=after_hooks, **ctx.obj)
