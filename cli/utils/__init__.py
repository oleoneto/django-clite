# cli:utils
import os
import click
from cli.logger import logger


PREVIOUS_WORKING_DIRECTORY = '..'


# Wrappers for `cd` and `mkdir`

def change_directory(directory, **kwargs):
    message = f"Change to directory [b]{directory}"

    logger.log(message, is_visible=kwargs.get('verbose', None), **kwargs)

    if kwargs.get('dry', None):
        return False

    os.chdir(directory)
    return True


def make_directory(directory, **kwargs):
    message = f"Create directory [b]{directory}"

    logger.log(message, is_visible=kwargs.get('verbose', None), **kwargs)

    if kwargs.get('dry', None):
        return False

    os.mkdir(directory)
    return True


def make_directories(directories, **kwargs):
    for directory in directories:
        make_directory(directory)


# Directory inspector

def inside_project_directory(ctx, exit_on_error=False):
    project_files = ['manage.py', 'wsgi.py', 'asgi.py']

    for file in project_files:
        if ctx.obj['project_files'].get(file, None):
            return True

    logger.error('Unable to locate project files.\nTry running this command at the top level of your project directory.')
    if exit_on_error:
        raise click.Abort

    return False


def inside_app_directory(ctx, exit_on_error=False):
    app_files = ['apps.py']

    for file in app_files:
        if ctx.obj['project_files'].get(file, None):
            return True

    logger.error('Not inside an app directory')
    if exit_on_error:
        raise click.Abort

    return False
