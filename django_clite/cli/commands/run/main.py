import click
import os
from django_clite.cli import find_management_file, log_error
from .helpers import (
    BuildHelper,
    FixtureHelper,
    MigrationHelper,
    ServerHelper
)

DEFAULT_MISSING_ARGS_ERROR = 'Missing arguments: {}.'
DEFAULT_TOO_MANY_ARGS_ERROR = 'Too many arguments passed.'


def not_an_app_directory_warning():
    if not ('apps.py' in os.listdir('.')):
        log_error("Not inside an app directory")
        raise click.Abort


def not_in_project_warning():
    path, management, code = find_management_file(os.getcwd())
    if not management:
        log_error('Cannot find manage.py in directory')
        raise click.Abort


@click.group()
@click.pass_context
def run(ctx):
    """
    Run maintenance, development, and deployment scripts.
    """

    not_in_project_warning()

    ctx.ensure_object(dict)

    p, m, c = find_management_file(os.getcwd())

    ctx.obj['path'] = p
    ctx.obj['management'] = m
    ctx.obj['code'] = c


# @run.command()
@click.pass_context
def build(ctx):
    """
    Run migrations and collect static files.
    """

    path = ctx.obj['management']
    BuildHelper.start(path)


# @run.command()
@click.pass_context
def deploy(ctx):
    """
    Push your project to your deployment server.

    This will prepare your project for deployment and run some checks for you. For example, the CLI will check if
    DEBUG or SECRET_KEY are properly configured. It will check if you have pending migrations and also collect
    staticfiles to your specified staticfiles location.

    First define your deployment upstream so the CLI can push your code to it. Once that is defined,
    in .config/upstream, the CLI will use the upstream server information to deploy your code.

    Supported deployment upstreams:
    - Dokku

    \b
        Define your upstream as DOKKU and add a DOKKU_HOST in your upstream configuration.
        The host needs to be an IP or fully qualified domain name (FQDN) for your upstream server.

    - Bitbucket, Github, and Gitlab

    \b
        Define your upstream as GIT and if your .git repository has an `origin` remote,
        the CLI will push your code to that server.
    """
    pass


# @run.command()
@click.pass_context
def docker(ctx):
    """
    Run project from within a Docker container.
    """
    pass


# @run.command()
@click.pass_context
def export_dokku_env(ctx):
    """
    Export all environment variables for DOKKU. Exported variables will look like so:

    \b
    dokku config:set --no-restart PROJECT_NAME VARIABLE=value
    """

# @run.command()
@click.option('-a', '--app', type=str, required=True, help='The app whose fixtures we must load.')
@click.option('-r', '--recursive', is_flag=True, help='Load all fixtures in directory.')
@click.argument('fixture', required=False)
@click.pass_context
def load_data(ctx, app, recursive, fixture):
    """
    Load data from fixtures.

    Loads all data contained in either .yaml or .json file within the fixtures directory of the specified app. For example:

    \b
        D run load-data --app blog articles
    
    This will load the articles.json or articles.yaml fixtures into the database.

    By specifying the --recursive flag, one can load all fixtures contained within the app's fixtures directory.
    """

    if recursive and fixture:
        log_error(DEFAULT_TOO_MANY_ARGS_ERROR)
        raise click.Abort
    elif not recursive and not fixture:
        log_error(DEFAULT_MISSING_ARGS_ERROR.format('--fixture or --recursive'))
        raise click.Abort
    
    path = ctx.obj['path']
    management = ctx.obj['management']
    
    print(path)
    print(management)


# @run.command()
@click.option('-a', '--app', type=str, required=False)
@click.option('--up/--down', default=True, help='Make or undo migrations.')
@click.option('-g', '--general', is_flag=True, help='Run migrations for all apps.')
@click.argument('options', nargs=-1, required=False)
@click.pass_context
def migrations(ctx, app, general, up, options):
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

    if not app and not general:
        log_error(DEFAULT_MISSING_ARGS_ERROR.format('--app or --general'))
        raise click.Abort

    path = ctx.obj['management']

    MigrationHelper.run(path, app, general, up, options)


@run.command()
@click.option('-p', '--port', type=int, required=False, help='The port the server will listen on.')
@click.pass_context
def server(ctx, port):
    """
    Runs the development server.
    """

    path = ctx.obj['management']

    ServerHelper.start(path, port)
