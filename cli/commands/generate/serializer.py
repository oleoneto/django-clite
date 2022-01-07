import click
from cli.commands.generate.helpers import resource_generator


@click.command()
@click.argument("name", required=True)
@click.pass_context
def serializer(ctx, name):
    """
    Generates a serializer for a given model.

    Checks for the existence of the specified model in models.py
    before attempting to create a serializer for it. Aborts if model is not found.
    """

    resource_generator(name, template='serializer.tpl', package='serializers', **ctx.obj)
