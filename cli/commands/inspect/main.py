import click
import os
from cli.helpers import get_project_name
from cli.helpers import find_project_files
from cli.helpers import not_in_project
from cli.helpers.logger import log_error
from cli.helpers.logger import DEFAULT_DIRECTORY_ERROR
from cli.commands.inspect.helpers import InspectorHelper


@click.command(name='show')
@click.option('--paths', is_flag=True, help="Show app paths.")
@click.option('--suppress-output', is_flag=True, help="Do not print to stdout.")
@click.argument('scope', required=True, type=click.Choice([
    'apps', 'admin', 'fixtures', 'forms', 'managers', 'models', 'serializers', 'viewsets']
))
@click.pass_context
def inspect(ctx, scope, paths, suppress_output):
    """
    Inspect your Django project.
    """

    ctx.ensure_object(dict)

    p, m, f = find_project_files(os.getcwd())

    ctx.obj['path'] = p
    ctx.obj['file'] = f
    ctx.obj['management'] = m
    ctx.obj['project'] = get_project_name(f)

    if not_in_project(ctx):
        log_error(DEFAULT_DIRECTORY_ERROR)
        raise click.Abort

    try:
        helper = InspectorHelper(
            cwd=m,
            dry=ctx.obj['dry'],
            verbose=ctx.obj['verbose'],
        )

        if scope == 'apps':
            return helper.get_apps(show_paths=paths, suppress_output=suppress_output)

        return helper.get_classes(scope=scope, show_paths=paths)
    except (AttributeError, FileNotFoundError, KeyError, TypeError) as e:
        log_error('An error occurred while running the command!')
