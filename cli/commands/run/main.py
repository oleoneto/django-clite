import click
from cli.utils.fs.utils import inside_project_directory
from cli.commands.run.helpers import make_migrations, migrate, run_server, run_copy_environment

DEFAULT_MISSING_ARGS_ERROR = 'Missing arguments: {}.'

DEFAULT_TOO_MANY_ARGS_ERROR = 'Too many arguments passed.'


@click.group()
@click.pass_context
def run(ctx):
    """
    Run maintenance, development, and deployment scripts.
    """

    ctx.ensure_object(dict)

    ctx.obj['scoped_context'] = {
        'verbose': ctx.obj['verbose'],
        'force': ctx.obj['force'],
        'dry': ctx.obj['dry'],
    }

    if not inside_project_directory(ctx, exit_on_error=not ctx.obj['force']):
        click.Abort()


@run.command()
@click.pass_context
@click.option('-f', '--filepath', type=click.Path(exists=True), required=False, help='Path to environment file.')
@click.option('--no-dokku', is_flag=True, help='Skip dokku export.')
@click.option('--no-example', is_flag=True, help='Skip example export.')
def export_env(ctx, filepath, no_dokku, no_example):
    """
    Export environment variables.
    Use this command to export environment variables to an example file or a dokku config file.
    For example environment file, all values are striped out, only keys are exported.

    \b
    In .env-dokku file:
    dokku config:set --no-restart PROJECT_NAME VARIABLE1=value1
    dokku config:set --no-restart PROJECT_NAME VARIABLE2=value2

    \b
    In .env-example file:
    VARIABLE1=
    VARIABLE2=

    The CLI assumes that your environment file lives next to the management file (manage.py).
    If that is not the case for your project, your can specify the path for the environment file
    (or just its name if in current directory) by passing the -f, --filepath option:

    \b
    D run export-env -f [filepath]
    """

    path = ctx.obj['project_files'].get('manage.py')

    try:
        run_copy_environment(
            path=path.parent,
            destination=path.parent,
            project_name=path.parent.name,
            filepath=filepath,
            no_dokku=no_dokku,
            no_example=no_example
        )
    except FileNotFoundError:
        click.Abort()


@run.command()
@click.option('-a', '--app', type=str, required=False)
@click.argument('options', nargs=-1, required=False)
@click.pass_context
def migrations(ctx, app, options):
    """
    Run database migrations.

    This combines both `makemigrations` and `migrate` commands into one. For example:

        D run migrations blog
    
    will accomplish the same as the following two commands:

    \b
        ./manage.py makemigrations blog && \\
        ./manage.py migrate blog

    Another thing this command seeks to accomplish is to bypass the need to navigate to
    the top of the directory in order to have access to the `manage.py` module. As long
    as the command is ran from within one of the following scopes, the command will work as intended:

    \b
        /project
        /project/project
        /project/project/app

    """

    path = ctx.obj['project_files'].get('manage.py')

    if app:
        make_migrations(path.parent, app, options)
        migrate(path.parent, app, options=options)
    else:
        make_migrations(path.parent, app=None, options=options)
        migrate(path.parent, app=None, options=options)


@run.command()
@click.option('-p', '--port', type=int, required=False, help='The port the server will listen on.')
@click.option('--plus', is_flag=True)
@click.pass_context
def server(ctx, port, plus):
    """
    Runs the development server.
    """

    path = ctx.obj['project_files'].get('manage.py')

    run_server(cwd=path.parent, path=path, port=port, plus=plus)
