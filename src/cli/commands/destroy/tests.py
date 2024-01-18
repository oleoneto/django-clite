import click
import inflection

from geny.core.filesystem.files import File
from cli.commands.callbacks import sanitized_string, sanitized_string_callback
from cli.decorators.scope import scoped, Scope
from cli.core.logger import logger
from cli.commands import command_defaults


SUPPORTED_SCOPES = [
    "model",
    "viewset",
]


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--scope", required=True, type=click.Choice(SUPPORTED_SCOPES))
@click.option("--full", is_flag=True, help=f"Destroy tests for {SUPPORTED_SCOPES}")
@click.pass_context
def test(ctx, name, scope, full):
    """
    Destroy TestCases.
    """

    if scope and full:
        logger.error("Flags --scope and --full cannot be used simultaneously.")
        raise click.Abort()

    scopes = SUPPORTED_SCOPES if full else [scope]

    for s in scopes:
        file = File(name=f"{inflection.pluralize(s)}/{sanitized_string(name)}_test.py")
        file.destroy(**{"import_statement": command_defaults.test(name), **ctx.obj})
