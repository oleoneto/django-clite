"""
Django CLI

Requirements:
Python3.6, PIP, Django 2.1, and Git

Description:
A CLI that handles creating and managing Django projects
"""

import click
import os
from djangocli.cli.commands.configurator.main import configure
from djangocli.cli.commands.destroyer.main import destroy
from djangocli.cli.commands.generator.main import generate
from djangocli.cli.commands.initializer.main import new
from djangocli.cli.commands.installer.main import install
from djangocli.cli.commands.migrator.main import db


@click.group()
@click.pass_context
def main(ctx):
    """
    Django CLI \f Version 0.0.alpha1
    """


"""
Commands should be added as sub-commands of the main click group.
This ensures sub-commands can be chained and 
run as `django-cli SUB-COMMAND COMMAND`
"""
# main.add_command(configure)
# main.add_command(db)
# main.add_command(destroy)
main.add_command(generate)
# main.add_command(new)
# main.add_command(install)

if __name__ == '__main__':
    main()
