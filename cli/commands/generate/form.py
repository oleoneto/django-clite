import click
from cli.commands.generate.helpers import resource_generator


@click.command()
@click.argument("name", required=True)
@click.pass_context
def form(ctx, name):
    """
    Generates a model form within the forms package.
    """

    resource_generator(name, template='form.tpl', package='forms', **ctx.obj)
