import click
import shutil


@click.group()
@click.pass_context
def new(ctx):
    """
    Creates new apps and projects
    """
    pass


@new.command()
@click.argument('name')
def app(name):
    """
    Creates a new app
    """
    pass


@new.command()
@click.argument('name')
def project(name):
    """
    Creates a new project
    """
    pass


@new.command()
@click.argument('name')
def requirement(name):
    """
    Adds new requirement to project
    """
    pass
