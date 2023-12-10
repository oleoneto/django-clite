import click
from .defaults.app import application_callback


@click.command()
@click.argument("names", nargs=-1, callback=application_callback)
@click.option("--is-package", is_flag=True)
@click.pass_context
def app(ctx, names, is_package):
    """
    Create djando apps.
    """

    [a.create() for a in names]
