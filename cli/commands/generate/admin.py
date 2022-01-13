import click
from cli.utils.sanitize import sanitized_string_callback
from cli.commands.generate.helpers import resource_generator


@click.command()
@click.argument('name', callback=sanitized_string_callback)
@click.argument("fields", nargs=-1, required=False)
@click.option('--inline', is_flag=True, help='Register admin model as inline.')
@click.option('--permissions', is_flag=True, help='Add permission stubs to admin model.')
@click.pass_context
def admin(ctx, name, fields, inline, permissions):
    """
    Generates an admin model within the admin package.
    """

    if inline:
        resource_generator(
            name,
            template='admin_inline.tpl',
            parent='admin',
            package='inlines',
            import_context={'classname': f"{name.capitalize()}Inline"},
            **ctx.obj
        )
    else:
        resource_generator(
            name,
            template='admin.tpl',
            package='admin',
            import_context={'classname': f"{name.capitalize()}Admin"},
            context={
                'fields': fields,
                'permissions': permissions,
            },
            **ctx.obj
        )
