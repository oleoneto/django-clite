import click

from geny.core.filesystem.files import File
from cli.commands.callbacks import sanitized_string_callback
from cli.decorators.scope import scoped, Scope
from cli.commands import command_defaults


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def tag(ctx, name, skip_import):
    """
    Generate a template tag.
    """

    file = File(
        name=f"templatetags/{name}.py",
        template="templatetags/tag.tpl",
        context={
            "name": name,
        },
    )

    file.create(
        import_statement=command_defaults.tag(name),
        add_import_statement=not skip_import,
        **ctx.obj,
    )
