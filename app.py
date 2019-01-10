"""
Django CLI

Requirements:
Python3.6, PIP, Django 2.1, and Git

Description:
A CLI that handles creating and managing Django projects
"""

import click
from djangocli.cli import AliasedGroup
from djangocli.cli.commands.destroyer.main import destroy
from djangocli.cli.commands.generator.main import generate


@click.command(cls=AliasedGroup)
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
main.add_command(destroy)
main.add_command(generate)

if __name__ == '__main__':
    main()
