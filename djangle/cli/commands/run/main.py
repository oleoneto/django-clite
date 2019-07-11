import click
import os
from djangle.cli import find_management_file, log_error


def not_an_app_directory_warning(ctx):
    if not ('apps.py' in os.listdir('.')):
        log_error("Not inside an app directory")
        raise click.Abort


@click.group()
@click.pass_context
def run(ctx):
    """
    Run maintenance, development, and deployment scripts.
    """
    not_an_app_directory_warning(ctx)

    ctx.ensure_object(dict)
    ctx.obj['path'] = find_management_file(os.getcwd())


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
    Initialize and run a Docker container.
    """
    pass


@run.command()
@click.pass_context
def migrations(ctx):
    """
    Run database migrations.

    This is combines both `makemigrations` and `migrate` commands into one.
    """
    pass


@run.command()
@click.pass_context
def server(ctx):
    """
    Runs the default Django server for your project.
    """
    pass
