"""
django-dj

Description:
A CLI that handles creating and managing Django projects
"""

import click
from djangle import AliasedGroup
from djangle.cli.commands import destroy
from djangle.cli.commands import generate
from djangle.cli.commands import new
from djangle.cli.commands import run


CONTEXT_SETTINGS = dict(token_normalize_func=lambda x: x.lower())


@click.command(cls=AliasedGroup)
@click.pass_context
def main(ctx):
    """
    django-dj

    A CLI to handle the creation and management of your Django projects.
    The CLI has some options about how your project should be structured in order for it to maximize the
    amount of automatic configuration it can provide you. Since Django itself adheres to configuration over
    convention, you are free to bypass conventions of the CLI if you so choose.
    """


"""
Commands should be added as sub-commands of the main click group.
This ensures sub-commands can be chained and
run as `django-dj SUB-COMMAND COMMAND`
"""
main.add_command(destroy)
main.add_command(generate)
main.add_command(new)
main.add_command(run)

if __name__ == '__main__':
    main()
