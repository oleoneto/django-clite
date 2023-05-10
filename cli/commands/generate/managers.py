import click
import logging
from cli.utils import sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser
from cli.logger import logger


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def manager(ctx, name):
    """
    Generate a model manager.
    """

    file = File(
        path=f"models/managers/{name}.py",
        template="models/manager.tpl",
        context={
            "name": name,
        },
    )

    # TODO: Revise the related template file under manager.tpl

    FileSystem().create_file(
        file=file,
        content=TemplateParser().parse_file(
            filepath=file.template, variables=file.context
        ),
    )
