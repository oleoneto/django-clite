import click
import inflection

from cli.utils import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope

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
        File(name=f"views/{name}{'_' + k if k else ''}.py").destroy(**ctx.obj)

    if include_templates:
        for class_ in classes:
            ctx.invoke(template, name=name, class_=class_)
