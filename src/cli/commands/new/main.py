import click

from cli.commands.new.app import apps
from cli.commands.new.project import project


@click.group()
@click.pass_context
def new(ctx):
    """
    Create projects and apps.
    """

    ctx.ensure_object(dict)


[new.add_command(cmd) for cmd in [apps, project]]
