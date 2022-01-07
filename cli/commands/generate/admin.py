import click
from cli.utils.sanitize import sanitized_string


@click.command()
@click.argument('name')
@click.option('--inline', is_flag=True, help='Register admin model as inline.')
@click.option('--stub-permissions', is_flag=True, help='Add permission stubs to admin model.')
@click.argument("fields", nargs=-1, required=False)
@click.pass_context
def admin(ctx, name, inline, fields, stub_permissions):
    """
    Generates an admin model within the admin package.
    """

    fields = [f for f in fields]

    sanitized_name = sanitized_string(name)
    classname = ""

    templates = [Template(f"{sanitized_name}.py", 'admin.tpl')]

    try:
        # Parse template
        content = template_handler.parsed_template(template='', context={})

        # Create admin file
        file_handler.create_file(content, filename=f"{sanitized_name}.py")

        # Append to admin/__init__.py file
        file_handler.append_to_file(filename='__init__.py', content=f"from .{sanitized_name} import {classname}Admin\n")
    except (KeyboardInterrupt, SystemExit):
        pass

    # try:
    #     if inline:
    #         path = ctx.obj['admin_inlines']
    #
    #     helper = AdminHelper(
    #         cwd=path,
    #         dry=ctx.obj['dry'],
    #         force=ctx.obj['force'],
    #         verbose=ctx.obj['verbose']
    #     )
    #
    #     helper.create(
    #         model=name,
    #         fields=fields,
    #         inline=inline,
    #         permissions=stub_permissions,
    #     )
    # except (KeyboardInterrupt, SystemExit):
    #     log_error('Exited!')
