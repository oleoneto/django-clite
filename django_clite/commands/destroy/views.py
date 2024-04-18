import click

from geny.core.filesystem.files import File
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
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
    "--include-templates",
    is_flag=True,
    default=False,
    help="Destroy related templates.",
)
@click.pass_context
def view(ctx, name, class_, full, include_templates):
    """
    Destroy a view function or class.
    """

    classes = SUPPORTED_CLASSES if full else [class_]

    for k in classes:
        File(name=f"views/{name}{'_' + k if k else ''}.py").destroy(
            **{
                "import_statement": command_defaults.view(name, k),
                **ctx.obj,
            }
        )

    if include_templates:
        for class_ in classes:
            ctx.invoke(template, name=name, class_=class_)
