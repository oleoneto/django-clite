import click
import inflection

from pathlib import Path
from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import RemoveLineFromFile
from django_clite.core.logger import logger
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback


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
        file = File(name=f"tests/{inflection.pluralize(s)}/{name}_test.py")

        file.destroy(
            after_hooks=[
                RemoveLineFromFile(
                    Path(f"tests/{inflection.pluralize(s)}/__init__.py"),
                    command_defaults.test(name),
                ),
            ],
            **ctx.obj,
        )
