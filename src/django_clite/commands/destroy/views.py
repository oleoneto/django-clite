import click

from pathlib import Path
from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import RemoveLineFromFile
from django_clite.decorators.scope import scoped, Scope
from .. import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback
from .template import template


SUPPORTED_CLASSES = [
    "create",
    "detail",
    "list",
    "update",
]


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--class_", type=click.Choice(SUPPORTED_CLASSES))
@click.option("--full", is_flag=True, help="Delete all CRUD views")
@click.option(
    "--keep-templates",
    is_flag=True,
    default=False,
    help="Destroy related templates.",
)
@click.pass_context
def view(ctx, name, class_, full, keep_templates):
    """
    Destroy a view function or class.
    """

    classes = SUPPORTED_CLASSES if full else [class_]

    for k in classes:
        File(name=f"views/{name}{'_' + k if k else ''}.py").destroy(
            after_hooks=[
                RemoveLineFromFile(
                    Path("views/__init__.py"),
                    command_defaults.view(name, klass=k),
                ),
            ],
            **ctx.obj,
        )

    if keep_templates:
        return

    for class_ in classes:
        ctx.invoke(template, name=name, class_=class_)
