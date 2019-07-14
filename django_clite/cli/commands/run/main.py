import click
import os
from django_clite.cli import find_management_file, log_error
from .helpers import RunnerHelper


def not_an_app_directory_warning():
    if not ('apps.py' in os.listdir('.')):
        log_error("Not inside an app directory")
        raise click.Abort


@click.group()
@click.pass_context
def run(ctx):
    """
    Run maintenance, development, and deployment scripts.
    """

    ctx.ensure_object(dict)
    ctx.obj['path'], b = find_management_file(os.getcwd())
    print(ctx.obj['path'])


@run.command()
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
def docker(ctx):
    """
    Run project from within a Docker container.
    """
    pass


@run.command()
@click.argument('app-name')
@click.pass_context
def migrations(ctx, app_name):
    """
    Run database migrations.

    This is combines both `makemigrations` and `migrate` commands into one. For example:

        D run migrations blog
    
    will accomplish the same as the following two commands:

    \b
        ./manage.py makemigrations blog && \\
        ./manage.py migrate blog

    Another thing this command seeks to accomplish is to bypass the need to navigate to
    the top of the directory in order to have access to the `manage.py` module. As long
    as the command is ran from within of the three scopes, the command will work as intended:

    \b
        /project
        /project/project
        /project/project/app

    """
    pass


@run.command()
@click.option('-w', '')
@click.pass_context
def server(ctx):
    """
    Runs the default Django server for your project or another one of choice.
    """
    pass
