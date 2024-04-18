import click

from geny.core.filesystem.files import File
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def tag(ctx, name):
    """
    Generate a template tag.
    """

    File(name=f"templatetags/{name}.py").destroy(
        **{
            "import_statement": command_defaults.tag(name),
            **ctx.obj,
        }
    )
