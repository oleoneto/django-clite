"""
Django CLI

Requirements:
Python3.6, PIP, Django 2.1, and Git

Description:
A CLI that handles creating and managing Django projects
"""

import click
from djangocli.cli.commands.generator.main import generate


@click.group()
@click.pass_context
def main(ctx):
    """
    Django CLI \f
    Version 0.0.1
    """


"""
Commands should be added as sub-commands of the main click group.
This ensures sub-commands can be chained and run as `django-cli SUB-COMMAND COMMAND`
"""
# main.add_command(commands.configurator)
# main.add_command(destroy)
# main.add_command(db)
# main.add_command(initializer)
# main.add_command(install)

# main.add_command()

if __name__ == '__main__':
    main()
