import click

from cli.commands.callbacks import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope
from cli.commands import command_defaults


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--full", is_flag=True, help="Destroy related files (i.e. TestCases)")
@click.pass_context
def viewset(ctx, name, full):
    """
    Destroy a viewset for a serializable model.
    """

    File(name=f"viewsets/{name}.py").destroy(
        **{
            "import_statement": command_defaults.viewset(name),
            **ctx.obj,
        }
    )

    if full:
        from .tests import test as cmd

        ctx.invoke(cmd, name=name, scope="viewset")
