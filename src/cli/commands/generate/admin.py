import click
import inflection

from cli.commands.callbacks import sanitized_string_callback, fields_callback
from cli.core.filesystem.files import File
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope
from cli.commands import command_defaults


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
        name=f"admin/{name}.py",
        template="admin/admin.tpl",
        context={
            "classname": inflection.camelize(name),
            "fields": admin_fields,
            "name": name,
            "permissions": permissions,
        },
    )

    file.create(
        import_statement=command_defaults.admin(name),
        add_import_statement=not skip_import,
        **ctx.obj,
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
        name=f"admin/inlines/{name}.py",
        template="admin/inline.tpl",
        context={
            "classname": inflection.camelize(name),
            "name": name,
        },
    )

    file.create(
        import_statement=command_defaults.admin_inline(name),
        add_import_statement=not skip_import,
        **ctx.obj,
    )
