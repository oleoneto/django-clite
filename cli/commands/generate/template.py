import click
from cli.commands.generate.helpers import resource_generator
from cli.utils.sanitize import sanitized_string


SUPPORTED_VIEW_TYPES = [
    'create',
    'detail',
    'list',
    'update',
]


@click.command()
@click.argument("name", required=True)
@click.option("-c", "--class-type", type=click.Choice(SUPPORTED_VIEW_TYPES))
@click.option('--full', is_flag=True, help='Create templates for all CRUD operations')
@click.pass_context
def template(ctx, name, class_type, full):
    """
    Generates an html template.
    """

    def generate_template(n, ct):
        resource_name = sanitized_string(n)
        filename = f"{resource_name}{'_' + ct if ct else ''}.html"
        scope = f"{'_' + ct if ct else ''}"

        resource_generator(
            resource_name,
            package='templates',
            filename=filename,
            template=f"template{scope}.tpl",
            no_append=True,
            scope='',
            **ctx.obj,
        )

    if full:
        [generate_template(name, t) for t in SUPPORTED_VIEW_TYPES]
    else:
        generate_template(name, class_type)


@click.command(name='tag')
@click.argument("name", required=True)
@click.pass_context
def templatetag(ctx, name):
    """
    Generates a template tag.
    """

    resource_generator(
        name,
        package='templatetags',
        template='templatetag.tpl',
        import_template="""from .{{ module }} import {{ module }}""",
        scope='', **ctx.obj,
    )
