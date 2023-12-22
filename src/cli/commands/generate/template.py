import click
import inflection

from cli.commands.callbacks import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope


SUPPORTED_CLASSES = [
    "create",
    "detail",
    "list",
    "update",
]


@scoped(to=Scope.APP)
@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--class_", type=click.Choice(SUPPORTED_CLASSES))
@click.option("--full", is_flag=True, help="Create templates for all CRUD operations")
@click.pass_context
def template(ctx, name, class_, full):
    """
    Generate an html template.
    """

    classes = SUPPORTED_CLASSES if full else [class_]

    for k in classes:
        file = File(
            name=f"templates/{name}{'_' + k if k else ''}.html",
            template=f"templates/{k if k else 'template'}.tpl",
            context={
                "classname": inflection.camelize(name),
            },
        )

        file.create(**ctx.obj)
