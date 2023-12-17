import click
import inflection

from cli.utils import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def form(ctx, name):
    """
    Destroy a form.
    """

    File(name=f"forms/{name}.py").destroy(**ctx.obj)
