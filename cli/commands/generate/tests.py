import click
import logging
import inflection
from cli.utils import sanitized_string, sanitized_string_callback
from cli.core.filesystem import File
from cli.constants import FILE_SYSTEM_HANDLER_KEY
from cli.logger import logger

SUPPORTED_SCOPES = [
    "model",
    "viewset",
]


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--scope", required=True, type=click.Choice(SUPPORTED_SCOPES))
@click.option("--full", is_flag=True, help=f"Create tests for {SUPPORTED_SCOPES}")
@click.pass_context
def test(ctx, name, scope, full):
    """
    Generate TestCases.
    """

    handler = ctx.obj[FILE_SYSTEM_HANDLER_KEY]

    scopes = SUPPORTED_SCOPES if full else [scope]

    files = [
        File(
            path=f"{inflection.pluralize(s)}/{sanitized_string(name)}_test.py",
            template=f"{inflection.pluralize(s)}/test.tpl",
            content=None,
            context={},
        )
        for s in scopes
    ]

    # TODO: TemplateHandler
