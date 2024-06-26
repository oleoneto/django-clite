import click
import inflection

from geny.core.filesystem.files import File
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands.callbacks import sanitized_string_callback, fields_callback


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

    file = File(
        name=f"fixtures/{model}.json",
        template="fixture.tpl",
        context={
            "total": total,
            "fields": fields,
            "classname": inflection.camelize(model),
        },
    )

    file.create(**ctx.obj)
