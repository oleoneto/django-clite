import click
import inflection

from cli.utils.sanitize import sanitized_string
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer
from cli.commands.destroy.template import template


SUPPORTED_VIEW_TYPES = [
    'create',
    'detail',
    'list',
    'update',
]


@click.command()
@click.argument('name', required=True)
@click.option('-c', '--class-type', type=click.Choice(SUPPORTED_VIEW_TYPES))
@click.option('--full', is_flag=True, help='Destroy all related views')
@click.option('--skip-templates', is_flag=True, default=False, help='Skip destruction of related templates.')
@click.pass_context
def view(ctx, name, class_type, full, skip_templates):
    """
    Destroys a view.
    """

    def destroy(n, ct):
        n = sanitized_string(n)
        scope = f"{'_' + ct if ct else ''}"
        module = f"{n}{scope}"
        classname = f"{inflection.camelize(n)}{ct.capitalize()}View" if ct else f"{n}_view"
        import_template = """from .{{module}} import {{classname}}"""

        resource_destroyer(
            n,
            package='views',
            filename=f"{module}.py",
            import_template=import_template,
            import_context={'module': module, 'classname': classname},
            **ctx.obj,
        )

        if not skip_templates:
            ctx.invoke(template, name=n, class_type=ct)

    if full:
        [destroy(name, t) for t in SUPPORTED_VIEW_TYPES]
    else:
        destroy(name, class_type)
