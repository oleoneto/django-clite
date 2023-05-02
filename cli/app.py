import os
import click
from pathlib import Path
from cli.click import AliasedAndDiscoverableGroup
from cli.core import FS
from cli import VERSION


django_files = FS.find(
    path=Path(os.getcwd()),
    patterns=[
        "apps.py",
        "asgi.py",
        "manage.py",
        "wsgi.py",
    ],
)


@click.command(cls=AliasedAndDiscoverableGroup)
@click.option("--debug", is_flag=True, help="Enable debug logs.")
@click.option("--dry", is_flag=True, help="Do not modify the file system.")
@click.option("-f", "--force", is_flag=True, help="Override any conflicting files.")
@click.option("--verbose", is_flag=True, help="Enable verbosity.")
@click.version_option(version=VERSION)
@click.pass_context
def cli(ctx, debug, dry, force, verbose):
    """
    django-clite by Leo Neto

    A CLI to handle the creation and management of your Django projects.

    The CLI has some opinions about how your project should be structured in order for it to maximize the
    amount of automatic configuration it can provide you. Since Django itself is highly configurable,
    you are free to bypass conventions of the CLI if you so choose.
    """

    # Note for contributors:
    #
    # Commands are auto-discovered if they are placed under the commands directory.
    # But please be sure to do the following for this to work:
    #   1. Name your package and click command the same.
    #   2. Place your command definition within your package's main.py module
    #   3. Any sub-commands of your command should be added to the top-most command in the package's main.py module.
    #
    #   Access your command like so:
    #   `django-clite my-command my-command-sub-command`
    #
    #   If you would like to skip a plugin/command from being auto-discovered,
    #   simply rename the package by either prepending or appending any number of underscores (_).
    #   Any code contained within the package will be ignored.

    ctx.ensure_object(dict)

    ctx.obj["dry"] = dry
    ctx.obj["force"] = force
    ctx.obj["enable_verbosity"] = verbose
    ctx.obj["enable_debug"] = debug
    ctx.obj["django_files"] = django_files


if __name__ == "__main__":
    try:
        cli()
    except (KeyboardInterrupt, SystemExit) as e:
        click.echo(f"Exited! {repr(e)}")
