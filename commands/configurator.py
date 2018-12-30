import os
import click
from commands.helpers.echoer import file_created, file_exists, successful, error
from commands.helpers.new import enter_dir, make_dir, create_settings_local, create_static_dir, create_template_dir


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


