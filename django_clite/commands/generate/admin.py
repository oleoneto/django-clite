import pathlib

import click
import inflection

from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import AddLineToFile, TouchFile
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback, fields_callback
from django_clite.decorators.scope import scoped, Scope


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

    admin_fields = [attr_name for attr_name, v in fields.items() if v.supports_admin]

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

    after_hooks = [
        TouchFile('admin/__init__.py')
    ]

    if not skip_import:
        after_hooks.append(
            AddLineToFile(
                pathlib.Path('admin/__init__.py'),
                command_defaults.admin(name),
                prevent_duplicates=True,
            )
        )

    file.create(after_hooks=after_hooks, **ctx.obj)


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

    after_hooks = [
        TouchFile('admin/inlines/__init__.py')
    ]

    if not skip_import:
        after_hooks.append(
            AddLineToFile(
                pathlib.Path('admin/inlines/__init__.py'),
                command_defaults.admin_inline(name),
                prevent_duplicates=True,
            )
        )

    file.create(after_hooks=after_hooks, **ctx.obj)
