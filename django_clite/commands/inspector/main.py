import os
from .helpers import InspectorHelper
from django_clite.helpers import get_project_name
from django_clite.helpers import find_project_files
from django_clite.helpers.logger import *


def wrong_place_warning(ctx):
    if (ctx.obj['path'] and ctx.obj['project_name']) is None:
        log_error(DEFAULT_MANAGEMENT_ERROR)
        raise click.Abort


@click.group()
@click.pass_context
def inspect(ctx):
    """
    Inspect your Django project.
    """

    ctx.ensure_object(dict)

    p, m, f = find_project_files(os.getcwd())

    ctx.obj['path'] = p
    ctx.obj['file'] = f
    ctx.obj['management'] = m
    ctx.obj['project_name'] = get_project_name(f)

    wrong_place_warning(ctx)

    ctx.obj['helper'] = InspectorHelper(cwd=m)


@inspect.command()
@click.option('--paths', is_flag=True, help="Show app paths.")
@click.option('--no-stdout', is_flag=True, help="Do not print to stdout.")
@click.pass_context
def apps(ctx, paths, no_stdout):
    """
    Show your project apps.
    """

    return ctx.obj['helper'].get_apps(
        show_paths=paths,
        no_stdout=no_stdout
    )


@inspect.command()
@click.option('--paths', is_flag=True, help="Show app paths.")
@click.option('--no-stdout', is_flag=True, help="Do not print to stdout.")
@click.pass_context
def models(ctx, paths, no_stdout):
    """
    Show your project models.
    """

    return ctx.obj['helper'].get_models(
        show_paths=paths,
        no_stdout=no_stdout
    )
