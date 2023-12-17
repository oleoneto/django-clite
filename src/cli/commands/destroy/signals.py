import click

from cli.utils import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def signal(ctx, name):
    """
    Destroy a signal.
    """

    File(name=f"models/signals/{name}.py").destroy(**ctx.obj)
