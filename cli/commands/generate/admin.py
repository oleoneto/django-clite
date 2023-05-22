import click
import inflection
from cli.utils import sanitized_string, sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser


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

    file = File(
        path=f"admin/{name}.py",
        template="admin/admin.tpl",
        context={
            "classname": inflection.camelize(name),
            "fields": fields,
            "name": name,
            "permissions": permissions,
        },
    )

    FileSystem().create_file(
        file=file,
        content=TemplateParser().parse_file(
            filepath=file.template,
            variables=file.context,
        ),
    )


@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.pass_context
def admin_inline(ctx, name):
    """
    Generate an inline admin model.
    """

    file = File(
        path=f"admin/inlines/{name}.py",
        template="admin/inline.tpl",
        context={
            "classname": inflection.camelize(name),
            "name": name,
        },
    )

    FileSystem().create_file(
        file=file,
        content=TemplateParser().parse_file(
            filepath=file.template,
            variables=file.context,
        ),
    )
