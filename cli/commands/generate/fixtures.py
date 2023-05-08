import click
import logging
from cli.utils import sanitized_string, sanitized_string_callback
from cli.core.filesystem import File
from cli.constants import FILE_SYSTEM_HANDLER_KEY
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

    handler = ctx.obj[FILE_SYSTEM_HANDLER_KEY]

    files = File(
        path=f"fixtures/{name}.json",
        template="fixture.tpl",
        content=None,
        context={
            "total": total,
            "fields": fields,
        },
    )

    print(f"{total}, {fields}")

    # TODO: TemplateHandler
