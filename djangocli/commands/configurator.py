import os
import click

@click.group()
@click.pass_context
@click.option('--dry', help="Test-drive the command with no changes to your file structure")
def configure(dry):
    pass


@configure.command()
@click.argument('name')
def staticfiles(name):
    pass


@configure.command()
@click.argument('name')
def media(name):
    pass
