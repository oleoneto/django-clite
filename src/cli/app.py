import click
import logging
from pathlib import Path
from cli import VERSION
from cli.extensions.combined import AliasedAndDiscoverableGroup
from cli.core.filesystem.finder import core_project_files, project_and_app_names
from cli.constants import (
    DJANGO_FILES_KEY,
    ENABLE_DRY_RUN_KEY,
    ENABLE_DEBUG_KEY,
    ENABLE_FORCE_KEY,
    ENABLE_VERBOSITY_KEY,
    PROJECT_NAME_KEY,
    APPLICATION_NAME_KEY,
)
from cli.core.templates.template import TemplateParser


@click.command(cls=AliasedAndDiscoverableGroup)
@click.option("--debug", is_flag=True, help="Enable debug logs.")
@click.option("--dry", is_flag=True, help="Do not modify the file system.")
@click.option("-f", "--force", is_flag=True, help="Override any conflicting files.")
@click.option("--verbose", is_flag=True, help="Enable verbosity.")
@click.option("--project", help="Project name.")
@click.option("--app", help="Application name.")
@click.version_option(version=VERSION)
@click.pass_context
def cli(ctx, debug, dry, force, verbose, project, app):
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

    from rich.logging import RichHandler

    FORMAT = "[DRY] %(message)s" if dry else "%(message)s"

    logging.basicConfig(
        encoding="utf-8",
        level=logging.DEBUG if verbose else logging.INFO,
        format=FORMAT,
        handlers=[
            RichHandler(
                log_time_format="",
                show_path=False,
                show_level=False,
                enable_link_path=True,
                markup=True,
            )
        ],
    )

    django_files = core_project_files()
    project_name, app_name = project_and_app_names(django_files)

    TemplateParser(
        templates_dir=Path(__file__).resolve().parent / "template_files",
        context={
            "project": project or project_name,
            "app": app or app_name,
        },
    )

    ctx.obj[DJANGO_FILES_KEY] = django_files
    ctx.obj[ENABLE_DEBUG_KEY] = debug
    ctx.obj[ENABLE_DRY_RUN_KEY] = dry
    ctx.obj[ENABLE_FORCE_KEY] = force
    ctx.obj[ENABLE_VERBOSITY_KEY] = verbose
    ctx.obj[PROJECT_NAME_KEY] = project or project_name
    ctx.obj[APPLICATION_NAME_KEY] = app or app_name


if __name__ == "__main__":
    try:
        cli()
    except (KeyboardInterrupt, SystemExit) as e:
        click.echo(f"Exited! {repr(e)}")
