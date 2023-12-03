import click
from .defaults.app import application_callback


@click.command()
@click.argument("names", nargs=-1, callback=application_callback)
@click.pass_context
def app(ctx, names):
    """
    Create djando apps.
    """

    [a.create() for a in names]
