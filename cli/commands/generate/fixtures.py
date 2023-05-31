import click
import inflection

from cli.utils import sanitized_string, sanitized_string_callback, fields_callback
from cli.core.filesystem.files import File
from cli.core.filesystem.filesystem import FileSystem
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("model", required=True, callback=sanitized_string_callback)
@click.option("--total", default=1, help="Number of fixtures to be created.")
@click.argument("fields", nargs=-1, required=False, callback=fields_callback)
@click.pass_context
def fixture(ctx, model, total, fields):
    """
    Generate model fixtures.
    """

    fixture_fields, _ = fields

    file = File(
        path=f"fixtures/{model}.json",
        template="fixture.tpl",
        context={
            "total": total,
            "fields": fixture_fields,
            "classname": inflection.camelize(model),
        },
    )

    FileSystem().create_file(
        file=file,
        content=TemplateParser().parse_file(
            filepath=file.template,
            variables=file.context,
        ),
    )
