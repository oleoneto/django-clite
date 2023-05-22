import os
import logging
import click
from pathlib import Path
from cli.click import AliasedAndDiscoverableGroup
from cli import VERSION
from cli.core.filesystem import FileSystem, Finder
from cli.core.templates import TemplateParser
from cli.constants import (
    CLI_NAME_KEY,
    DJANGO_FILES_KEY,
    ENABLE_DRY_RUN_KEY,
    ENABLE_DEBUG_KEY,
    ENABLE_FORCE_KEY,
    ENABLE_VERBOSITY_KEY,
    FILE_SYSTEM_HANDLER_KEY,
    TEMPLATES_KEY,
)


@click.command(cls=AliasedAndDiscoverableGroup)
@click.option("--debug", is_flag=True, help="Enable debug logs.")
@click.option("--dry", is_flag=True, help="Do not modify the file system.")
@click.option("-f", "--force", is_flag=True, help="Override any conflicting files.")
@click.option("--verbose", is_flag=True, help="Enable verbosity.")
@click.option("--project", help="Project name.")
@click.option("--app", help="Application name.")
@click.option("--settings", help="Path to project's settings file.")
@click.version_option(version=VERSION)
@click.pass_context
def cli(ctx, debug, dry, force, verbose, project, app, settings):
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

    if verbose:
        logger.setLevel(logging.DEBUG)

    django_files = Finder().find(
        path=Path(os.getcwd()),
        patterns=[
            "apps.py",
            "asgi.py",
            "manage.py",
            "wsgi.py",
        ],
    )

    def names():
        for k, v in django_files.items():
            if k == "apps.py":
                return v.parent.parent.name, v.parent.name
            elif k in ["asgi.py", "manage.py", "wsgi.py"]:
                return v.parent.name, ""
        return "", ""

    project_name, app_name = names()

    fs = FileSystem(dry=dry, debug=debug, verbose=verbose, force=force)
    tp = TemplateParser(
        context={
            "project": project or project_name,
            "app": app or app_name,
        },
        templates_dir=Path(__file__).resolve().parent / "template_files",
    )

    ctx.obj[DJANGO_FILES_KEY] = django_files
    ctx.obj[ENABLE_DEBUG_KEY] = debug
    ctx.obj[ENABLE_DRY_RUN_KEY] = dry
    ctx.obj[ENABLE_FORCE_KEY] = force
    ctx.obj[ENABLE_VERBOSITY_KEY] = verbose


if __name__ == "__main__":
    try:
        cli()
    except (KeyboardInterrupt, SystemExit) as e:
        click.echo(f"Exited! {repr(e)}")
