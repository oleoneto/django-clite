import click
from cli.commands.generate.helpers import resource_generator


SUPPORTED_VIEW_TYPES = [
    'create',
    'detail',
    'list',
    'update',
    'template',
    'form',
]


@click.command()
@click.argument("name", required=True)
@click.option("-t", "--class-type", type=click.Choice(SUPPORTED_VIEW_TYPES))
@click.option('--full', is_flag=True, help='Create all CBVs for given resource')
@click.pass_context
def template(ctx, name, class_type, full):
    """
    Generates an html template.
    """

    # TODO: Handle generation of other template types

    resource_generator(
        name,
        template='template.tpl',
        package='templates',
        file_extension='.html',
        no_append=True,
        scope='',
        **ctx.obj,
    )


@click.command(name='tag')
@click.argument("name", required=True)
@click.pass_context
def templatetag(ctx, name):
    """
    Generates a template tag.
    """

    resource_generator(
        name,
        template='templatetag.tpl',
        import_template="""from .{{ module }} import {{ module }}""",
        package='templatetags',
        scope='', **ctx.obj,
    )
