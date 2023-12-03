import click
import inflection
from cli.utils import sanitized_string, sanitized_string_callback
from cli.core.filesystem.filesystem import File, FileSystem
from cli.core.templates.template import TemplateParser
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
@click.option("--klass", type=click.Choice(SUPPORTED_CLASSES))
@click.option("--full", is_flag=True, help="Create templates for all CRUD operations")
@click.pass_context
def template(ctx, name, klass, full):
    """
    Generate an html template.
    """

    klasses = SUPPORTED_CLASSES if full else [klass]

    for k in klasses:
        file = File(
            name=f"templates/{name}{'_' + k if k else ''}.html",
            template=f"templates/{k if k else 'template'}.tpl",
            context={
                "classname": inflection.camelize(name),
            },
        )

        FileSystem().create_file(
            file=file,
            content=TemplateParser().parse_file(
                filepath=file.template,
                variables=file.context,
            ),
        )
