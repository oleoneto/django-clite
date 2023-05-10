import click
import logging
from cli.utils import sanitized_string, sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser
from cli.logger import logger


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--total", default=1, help="Number of fixtures to be created.")
@click.argument("fields", nargs=-1, required=False)
@click.pass_context
def fixture(ctx, name, total, fields):
    """
    Generate model fixtures.
    """

    file = File(
        path=f"fixtures/{name}.json",
        template="fixture.tpl",
        context={
            "total": total,
            "fields": fields,
            "classname": "",
        },
    )

    FileSystem().create_file(
        file=file,
        content=TemplateParser().parse_file(
            filepath=file.template, variables=file.context
        ),
    )
