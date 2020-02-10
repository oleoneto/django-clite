import os
import click
from django_clite.helpers.logger import log_error
from django_clite.helpers import find_project_files
from django_clite.helpers import get_project_name
from django_clite.helpers import save_to_settings
from .helpers import (
    BuildHelper,
    EnvironmentHelper,
    MigrationHelper,
    ServerHelper,
    DockerHelper
)

DEFAULT_MISSING_ARGS_ERROR = 'Missing arguments: {}.'

DEFAULT_TOO_MANY_ARGS_ERROR = 'Too many arguments passed.'


def not_an_app_directory_warning():
    if not ('apps.py' in os.listdir('.')):
        log_error("Not inside an app directory")
        raise click.Abort


def not_in_project_warning():
    path, management, file = find_project_files(os.getcwd())
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

    p, m, f = find_project_files(os.getcwd())

    ctx.obj['path'] = p
    ctx.obj['management'] = m
    ctx.obj['file'] = f
    ctx.obj['project_name'] = get_project_name(f)


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

    helper = EnvironmentHelper(cwd=ctx.obj['management'])

    helper.run(
        path=ctx.obj['management'],
        project_name=ctx.obj['project_name'],
        filepath=filepath,
        destination=ctx.obj['management'],
        no_dokku=no_dokku,
        no_example=no_example
    )


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

    path = ctx.obj['management']

    MigrationHelper.run(path, app, options)


@run.command()
@click.option('-p', '--port', type=int, required=False, help='The port the server will listen on.')
@click.pass_context
def server(ctx, port):
    """
    Runs the development server.
    """
    helper = ServerHelper(cwd=ctx.obj['management'])

    helper.run(
        path=ctx.obj['management'],
        port=port
    )


# @run.command()
@click.option('-k', '--key', required=True, help='Parameter name.')
@click.option('-v', '--value', required=True, help='Parameter value.')
@click.pass_context
def update_setting(ctx, key, value):
    """
    Update project settings.
    """

    save_to_settings(
        value=f"{value}",
        parameter=key,
        path=ctx.obj['path']
    )


#######################################

@click.group()
@click.option('--create-config', is_flag=True, help='Create Dockerfile and docker-compose.yml')
@click.option('--verbose', is_flag=True, help='Run in verbose mode.')
@click.pass_context
def docker(ctx, verbose, create_config):
    """
    Run Docker-related options for your project.
    """

    ctx.obj['verbose'] = verbose

    ctx.obj['docker'] = DockerHelper(cwd=ctx.obj['management'])

    if create_config:
        ctx.invoke(create_dockerfile)
        ctx.invoke(create_compose)


@docker.command()
@click.pass_context
def build(ctx):
    """
    Build Docker container for this project.
    """

    return ctx.obj['docker'].build(verbose=ctx.obj['verbose'])


@docker.command()
@click.pass_context
def start(ctx):
    """
    Start Docker container for this project.
    """

    return ctx.obj['docker'].start(verbose=ctx.obj['verbose'])


@docker.command()
@click.pass_context
def create_dockerfile(ctx):
    """
    Creates a Dockerfile for this project.
    """

    return ctx.obj['docker'].create_dockerfile(
        project=ctx.obj['project_name']
    )


@docker.command()
@click.pass_context
def create_compose(ctx):
    """
    Creates a docker-compose file for this project.
    """

    return ctx.obj['docker'].create_compose(
        project=ctx.obj['project_name']
    )


run.add_command(docker)
