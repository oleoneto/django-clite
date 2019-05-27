"""
Django CLI

Description:
A CLI that handles creating and managing Django projects
"""

import click
from djangocli.cli import AliasedGroup
from djangocli.cli.commands.destroyer.main import destroy
from djangocli.cli.commands.generator.main import generate
from djangocli.cli.commands.creator.main import new


@click.command(cls=AliasedGroup)
@click.pass_context
def main(ctx):
    """
    Django CLI

    One CLI to handle the creation and management of your Django projects.
    """


"""
Commands should be added as sub-commands of the main click group.
This ensures sub-commands can be chained and
run as `django-cli SUB-COMMAND COMMAND`
"""
main.add_command(destroy)
main.add_command(generate)
main.add_command(new)

if __name__ == '__main__':
    main()
