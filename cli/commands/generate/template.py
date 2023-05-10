import click
import logging
from cli.utils import sanitized_string, sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser
from cli.logger import logger

SUPPORTED_CLASSES = [
    "create",
    "detail",
    "list",
    "update",
]


@click.command()
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
            path=f"templates/{sanitized_string(name)}{'_' + k if k else ''}.html",
            template=f"templates/{k if k else 'template'}.tpl",
            context={},
        )

        FileSystem().create_file(
            file=file,
            content=TemplateParser().parse_file(
                filepath=file.template, variables=file.context
            ),
        )
