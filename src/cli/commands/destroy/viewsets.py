import click
import inflection

from cli.utils import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--full", is_flag=True, help="Destroy related files (i.e. TestCases)")
@click.pass_context
def viewset(ctx, name, full):
    """
    Destroy a viewset for a serializable model.
    """

    File(name=f"viewsets/{name}.py").destroy(**ctx.obj)

    if full:
        from .tests import test as cmd

        ctx.invoke(cmd, name=name, scope="viewset")
