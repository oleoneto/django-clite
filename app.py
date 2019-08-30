"""
django-clite

Description:
A CLI that handles creating and managing Django projects
"""

import click
from django_clite import AliasedGroup
from django_clite.cli.commands import create
from django_clite.cli.commands import destroy
from django_clite.cli.commands import generate
from django_clite.cli.commands import run


CONTEXT_SETTINGS = dict(token_normalize_func=lambda x: x.lower())


@click.command(cls=AliasedGroup)
@click.pass_context
def main(ctx):
    """
    django-clite

    A CLI to handle the creation and management of your Django projects.
    The CLI has some options about how your project should be structured in order for it to maximize the
    amount of automatic configuration it can provide you. Since Django itself adheres to configuration over
    convention, you are free to bypass conventions of the CLI if you so choose.
    """


"""
Commands should be added as sub-commands of the main click group.
This ensures sub-commands can be chained and
run as `django-clite SUB-COMMAND COMMAND`
"""
main.add_command(create)
main.add_command(destroy)
main.add_command(generate)
main.add_command(run)

if __name__ == '__main__':
    main()
