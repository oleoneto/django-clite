import click
import inflection
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
@click.option("-c", "--class-type", type=click.Choice(SUPPORTED_VIEW_TYPES))
@click.option('--full', is_flag=True, help='Create all CRUD views')
@click.option('--skip-templates', is_flag=True, default=False, help='Skip generation of related templates.')
@click.pass_context
def view(ctx, name, class_type, full, skip_templates):
    """
    Generates a view function or class.
    """

    def generate(n, ct):
        n = sanitized_string(n)
        scope = f"{'_' + ct if ct else ''}"
        module = f"{n}{scope}"
        template_name = f"{module}.html"
        classname = f"{inflection.camelize(n)}{ct.capitalize()}View" if ct else f"{n}_view"
        import_template = """from .{{module}} import {{classname}}"""

        resource_generator(
            n,
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
        if not skip_templates:
            ctx.invoke(template, name=n, class_type=ct)

    Directory.ensure_directory('views', **ctx.obj)

    if full:
        [generate(name, t) for t in SUPPORTED_VIEW_TYPES]
    else:
        generate(name, class_type)
