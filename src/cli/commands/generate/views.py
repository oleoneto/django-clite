import click
import inflection

from cli.commands.callbacks import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope
from cli.commands import command_defaults

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
@click.option("--full", is_flag=True, help="Create all CRUD views")
@click.option(
    "--skip-templates",
    is_flag=True,
    default=False,
    help="Skip generation of related templates.",
)
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def view(ctx, name, class_, full, skip_templates, skip_import):
    """
    Generate a view function or class.
    """

    classes = SUPPORTED_CLASSES if full else [class_]

    for k in classes:
        file = File(
            name=f"views/{name}{'_' + k if k else ''}.py",
            template=f"views/{k if k else 'view'}.tpl",
            context={
                "name": name,
                "classname": inflection.camelize(name),
                "namespace": inflection.pluralize(name),
                "template_name": f"{name}{'_' + k if k else ''}.hml",
            },
        )

        file.create(
            import_statement=command_defaults.view(name, k),
            add_import_statement=not skip_import,
            **ctx.obj,
        )

    if skip_templates:
        return

    for class_ in classes:
        ctx.invoke(template, name=name, class_=class_)
