import click
from cli.utils.sanitize import sanitized_string
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer


SUPPORTED_VIEW_TYPES = [
    'create',
    'detail',
    'list',
    'update',
]


@click.command()
@click.argument('name')
@click.option('-c', '--class-type', type=click.Choice(SUPPORTED_VIEW_TYPES))
@click.option('--full', is_flag=True, help='Destroy all related templates')
@click.pass_context
def template(ctx, name, class_type, full):
    """
    Destroys templates.
    """

    def destroy(n, ct):
        filename = f"{sanitized_string(n)}{'_' + ct if ct else ''}.html"

        resource_destroyer(
            n,
            filename=filename,
            package='templates',
            ignore_import=True,
            scope='',
            **ctx.obj,
        )

    if full:
        [destroy(name, t) for t in SUPPORTED_VIEW_TYPES]
    else:
        destroy(name, class_type)


@click.command(name='tag')
@click.argument("name", required=True)
@click.pass_context
def templatetag(ctx, name):
    """
    Destroys a template tag.
    """

    resource_destroyer(
        name,
        package='templatetags',
        import_template="""from .{{module}} import {{module}}""",
        **ctx.obj
    )
