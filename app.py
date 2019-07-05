"""
Djangle-CLI

Description:
A CLI that handles creating and managing Django projects
"""

import click
from djangle.cli import AliasedGroup
from djangle.cli.commands.creator.main import new
from djangle.cli.commands.destroyer.main import destroy
from djangle.cli.commands.generator.main import generate


@click.command(cls=AliasedGroup)
@click.pass_context
def main(ctx):
    """
    Djangle-CLI

    A CLI to handle the creation and management of your Django projects.
    """


"""
Commands should be added as sub-commands of the main click group.
This ensures sub-commands can be chained and
run as `djangle SUB-COMMAND COMMAND`
"""
main.add_command(destroy)
main.add_command(generate)
main.add_command(new)

if __name__ == '__main__':
    main()
