import click
from cli.click.mutex import Mutex
from cli.utils.sanitize import sanitized_string
from cli.commands.generate.helpers import resource_generator
from cli.handlers.filesystem.directory import Directory
from cli.commands.generate.template import template


SUPPORTED_VIEW_TYPES = [
    'create',
    'detail',
    'list',
    'update',
]


@click.command()
@click.argument("name", required=True)
@click.option("-c", "--class-type", type=click.Choice(SUPPORTED_VIEW_TYPES), cls=Mutex, not_required_if=["full"])
@click.option('--full', is_flag=True, help='Create all CRUD views', cls=Mutex, not_required_if=["class-type"])
@click.option('--no-template', is_flag=True, default=False, help='Generate related template.')
@click.pass_context
def view(ctx, name, class_type, full, no_template):
    """
    Generates a view function or class.
    """

    def generate_view(n, ct):
        resource_name = sanitized_string(n)
        scope = f"{'_' + ct if ct else ''}"
        module = f"{resource_name}{scope}"
        classname = f"{resource_name.capitalize()}{ct.capitalize()}View" if ct else f"{resource_name}_view"
        template_name = f"{resource_name}{scope}.html"
        import_template = """from .{{module}} import {{classname}}"""

        resource_generator(
            resource_name,
            package='views',
            filename=f"{module}.py",
            template=f"view{scope}.tpl",
            import_template=import_template,
            import_context={'module': module, 'classname': classname},
            context={
                'template_name': template_name,
            },
            **ctx.obj
        )

        # Handle creation of related template
        if not no_template:
            ctx.invoke(template, name=resource_name, class_type=ct)

    Directory.ensure_directory('views', **ctx.obj)

    if full:
        [generate_view(name, t) for t in SUPPORTED_VIEW_TYPES]
    else:
        generate_view(name, class_type)
