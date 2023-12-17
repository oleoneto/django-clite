import click

from cli.utils import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("model", required=True, callback=sanitized_string_callback)
@click.pass_context
def fixture(ctx, model):
    """
    Destroy model fixtures.
    """

    File(name=f"fixtures/{model}.json").destroy(**ctx.obj)
