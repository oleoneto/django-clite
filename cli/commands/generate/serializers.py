import click
import logging
from cli.utils import sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser
from cli.logger import logger


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def serializer(ctx, name):
    """
    Generate a serializer for a given model.

    Checks for the existence of the specified model in models.py
    before attempting to create a serializer for it. Aborts if model is not found.
    """

    file = File(
        path=f"serializers/{name}.py",
        template="serializer.tpl",
        context={
            "name": name,
            # TODO: Add model
            # TODO: Add ClassName
        },
    )

    FileSystem().create_file(
        file=file,
        content=TemplateParser().parse_file(
            filepath=file.template, variables=file.context
        ),
    )
