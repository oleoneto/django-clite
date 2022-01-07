import click
from cli.commands.generate.helpers import resource_generator
# from cli.commands.generate.


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
@click.option("-c", "--class-type", type=click.Choice(SUPPORTED_VIEW_TYPES))
@click.option('--no-template', is_flag=True, default=False, help='Generate related template.')
@click.option('--full', is_flag=True, help='Create all CBVs for given resource')
@click.pass_context
def view(ctx, name, class_type, no_template, full):
    """
    Generates a view function or class.
    """

    # resource_generator(name, template=f"view-{}.tpl", package='views', **ctx.obj)

    # if full:
    #     [helper.create(model=name, class_type=klass) for klass in SUPPORTED_VIEW_TYPES if klass not in 'template']
    #     # [resource_generator(name, template=f"", package='views', **kwargs) for k]
    #
    #     if not no_template:
    #         [ctx.invoke(template, name=name, class_type=klass) for klass in SUPPORTED_VIEW_TYPES]
    #
    # else:
    #     helper.create(model=name, class_type=class_type)
    #
    #     if not no_template:
    #         ctx.invoke(template, name=name, class_type=class_type)
