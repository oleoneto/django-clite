import click
import logging
import inflection
from cli.utils import sanitized_string, sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser
from cli.logger import logger

SUPPORTED_SCOPES = [
    "model",
    "viewset",
]


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--scope", type=click.Choice(SUPPORTED_SCOPES))
@click.option("--full", is_flag=True, help=f"Create tests for {SUPPORTED_SCOPES}")
@click.pass_context
def test(ctx, name, scope, full):
    """
    Generate TestCases.
    """

    scopes = SUPPORTED_SCOPES if full else [scope]

    for s in scopes:
        file = File(
            path=f"{inflection.pluralize(s)}/{sanitized_string(name)}_test.py",
            template=f"{inflection.pluralize(s)}/test.tpl",
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
