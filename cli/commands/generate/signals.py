import click
import logging
from cli.utils import sanitized_string_callback
from cli.core.filesystem import File
from cli.constants import FILE_SYSTEM_HANDLER_KEY
from cli.logger import logger


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def signal(ctx, name):
    """
    Generate a signal.
    """

    file = File(
        path=f"models/signals/{name}.py",
        template="models/signal.tpl",
        content=None,
        context={},
    )

    handler = ctx.obj[FILE_SYSTEM_HANDLER_KEY]

    # TODO: TemplateHandler
