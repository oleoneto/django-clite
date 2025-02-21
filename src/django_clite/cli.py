import click
import logging
from pathlib import Path

from rich.logging import RichHandler

from django_clite.extensions import AliasedAndDiscoverableGroup
from geny.core.filesystem.finder import core_project_files, project_and_app_names
from geny.core.templates.template import TemplateParser

from django_clite.constants import (
    DJANGO_FILES_KEY,
    ENABLE_DRY_RUN_KEY,
    ENABLE_DEBUG_KEY,
    ENABLE_FORCE_KEY,
    ENABLE_VERBOSITY_KEY,
    PROJECT_NAME_KEY,
    APPLICATION_NAME_KEY,
    TEMPLATES_DIRECTORY_ENV_VAR,
)


@click.command(
    cls=AliasedAndDiscoverableGroup, context_settings=dict(ignore_unknown_options=True)
)
@click.option("--debug", is_flag=True, help="Enable debug logs.")
@click.option("--dry", is_flag=True, help="Do not modify the file system.")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    envvar=ENABLE_FORCE_KEY,
    help="Override any conflicting files.",
)
@click.option("--verbose", is_flag=True, help="Enable verbosity.")
@click.option("--project", help="Project name.")
@click.option("--app", help="Application name.")
@click.option(
    "--templates-dir",
    "-t",
    envvar=TEMPLATES_DIRECTORY_ENV_VAR,
    help="Template directory.",
    type=click.Path(),
)
@click.version_option(package_name="django-clite")
@click.pass_context
def main(ctx, debug, dry, force, verbose, project, app, templates_dir):
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

    templates = [Path(__file__).resolve().parent / "template_files"]

    if templates_dir is not None:
        templates.append(Path(templates_dir))

    TemplateParser(
        templates_dir=templates,
        context={},
    )

    btx = {
        DJANGO_FILES_KEY: django_files,
        ENABLE_DEBUG_KEY: debug,
        ENABLE_DRY_RUN_KEY: dry,
        ENABLE_FORCE_KEY: force,
        ENABLE_VERBOSITY_KEY: verbose,
        PROJECT_NAME_KEY: project or project_name,
        APPLICATION_NAME_KEY: app or app_name,
    }

    ctx.ensure_object(dict)
    ctx.obj = btx


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        click.echo(f"Exited! {repr(e)}")
