import click
import pathlib
import inflection

from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import AddLineToFile, TouchFile
from django_clite.core.logger import logger
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string, sanitized_string_callback


SUPPORTED_SCOPES = [
    "model",
    "viewset",
]


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--scope", required=True, type=click.Choice(SUPPORTED_SCOPES))
@click.option("--full", is_flag=True, help=f"Create tests for {SUPPORTED_SCOPES}")
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def test(ctx, name, scope, full, skip_import):
    """
    Generate TestCases.
    """

    if scope and full:
        logger.error("Flags --scope and --full cannot be used simultaneously.")
        raise click.Abort()

    scopes = SUPPORTED_SCOPES if full else [scope]

    for s in scopes:
        filename = f"tests/{inflection.pluralize(s)}/{sanitized_string(name)}_test.py"

        file = File(
            name=filename,
            template=f"{inflection.pluralize(s)}/test.tpl",
            context={
                "name": name,
                "module": name,
                "classname": inflection.camelize(name),
                "namespace": inflection.pluralize(name),
                "scope": "" if scope is None else inflection.pluralize(scope),
            },
        )

        after_hooks = [
            TouchFile(f'tests/{inflection.pluralize(s)}/__init__.py')
        ]

        if not skip_import:
            after_hooks.append(
                AddLineToFile(
                    pathlib.Path(f'tests/{inflection.pluralize(s)}/__init__.py'),
                    command_defaults.test(name),
                    prevent_duplicates=True,
                )
            )

        file.create(after_hooks=after_hooks, **ctx.obj)
