import click
import logging
from cli.utils import sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser
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
        context={
            "name": name,
        },
    )

    FileSystem().create_file(
        file=file,
        content=TemplateParser().parse_file(
            filepath=file.template, variables=file.context
        ),
    )
