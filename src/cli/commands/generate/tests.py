import click
import inflection
from cli.utils import sanitized_string, sanitized_string_callback
from cli.core.filesystem.filesystem import File, FileSystem
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope
from cli.core.logger import logger


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
        file = File(
            name=f"{inflection.pluralize(s)}/{sanitized_string(name)}_test.py",
            template=f"{inflection.pluralize(s)}/test.tpl",
            context={
                "name": name,
                "module": name,
                "classname": inflection.camelize(name),
                "namespace": inflection.pluralize(name),
            },
        )

        FileSystem().create_file(
            file=file,
            content=TemplateParser().parse_file(
                filepath=file.template,
                variables=file.context,
            ),
            import_statement=TemplateParser().parse_string(
                content="from .{{module}} import {{classname}}TestCase",
                variables={
                    "module": name,
                    "classname": inflection.camelize(name),
                },
            ),
            add_import_statement=not skip_import,
        )
