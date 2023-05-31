import click
import inflection

from cli.utils import sanitized_string, sanitized_string_callback, fields_callback
from cli.core.filesystem.files import File
from cli.core.filesystem.filesystem import FileSystem
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.argument("fields", nargs=-1, required=False, callback=fields_callback)
@click.option(
    "--permissions", is_flag=True, help="Add permission stubs to admin model."
)
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def admin(ctx, name, fields, permissions, skip_import):
    """
    Generate an admin model.
    """

    admin_fields, _ = fields
    admin_fields = [x for x in admin_fields if x.supported_in_admin]

    file = File(
        path=f"admin/{name}.py",
        template="admin/admin.tpl",
        context={
            "classname": inflection.camelize(name),
            "fields": admin_fields,
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
        import_statement=TemplateParser().parse_string(
            content="from .{{name}} import {{classname}}Admin",
            variables={
                "name": name,
                "classname": inflection.camelize(name),
            },
        ),
        add_import_statement=not skip_import,
    )


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def admin_inline(ctx, name, skip_import):
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
        import_statement=TemplateParser().parse_string(
            content="from .{{name}} import {{classname}}Inline",
            variables={
                "name": name,
                "classname": inflection.camelize(name),
            },
        ),
        add_import_statement=not skip_import,
    )
