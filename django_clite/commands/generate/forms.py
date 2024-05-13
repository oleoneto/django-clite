import click
import pathlib
import inflection

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
def form(ctx, name, skip_import):
    """
    Generate a form.
    """

    file = File(
        name=f"forms/{name}.py",
        template="form.tpl",
        context={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )

    after_hooks = [
        TouchFile('forms/__init__.py')
    ]

    if not skip_import:
        after_hooks.append(
            AddLineToFile(
                pathlib.Path('forms/__init__.py'),
                command_defaults.form(name),
                prevent_duplicates=True,
            )
        )

    file.create(after_hooks=after_hooks, **ctx.obj)
