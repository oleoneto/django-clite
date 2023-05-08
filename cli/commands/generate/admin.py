import click
from cli.utils import sanitized_string, sanitized_string_callback
from cli.core.filesystem import File
from cli.constants import FILE_SYSTEM_HANDLER_KEY
from cli.logger import logger


@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.argument("fields", nargs=-1, required=False)
@click.option(
    "--permissions", is_flag=True, help="Add permission stubs to admin model."
)
@click.pass_context
def admin(ctx, name, fields, permissions):
    """
    Generate an admin model.
    """

    handler = ctx.obj[FILE_SYSTEM_HANDLER_KEY]

    files = File(
        path=f"admin/{name}.py",
        template="admin/admin.tpl",
        content=None,
        context={},
    )

    # TODO: TemplateHandler


@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.pass_context
def inline(ctx, name):
    """
    Generate an inline admin model.
    """

    handler = ctx.obj[FILE_SYSTEM_HANDLER_KEY]

    files = File(
        path=f"admin/inlines/{name}.py",
        template="admin/inline.tpl",
        content=None,
        context={},
    )

    # TODO: TemplateHandler
