import click
import inflection

from cli.utils import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def serializer(ctx, name):
    """
    Destroy a serializer for a given model.
    """

    File(name=f"serializers/{name}.py").destroy(**ctx.obj)
