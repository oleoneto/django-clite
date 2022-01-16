# cli:utils
import os
import click
from cli.utils.logger import Logger
from cli.utils.finders import find_project_files


PREVIOUS_WORKING_DIRECTORY = '..'


# Wrappers for `cd` and `mkdir`

def change_directory(directory, **kwargs):
    message = f"Change to directory [b]{directory}"

    Logger.log(message, is_visible=kwargs.get('verbose', None), **kwargs)

    if kwargs.get('dry', None):
        return False

    os.chdir(directory)
    return True


def make_directory(directory, **kwargs):
    message = f"Create directory [b]{directory}"

    Logger.log(message, is_visible=kwargs.get('verbose', None), **kwargs)

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

    Logger.error('Unable to locate project files.\nTry running this command at the top level of your project directory.')
    if exit_on_error:
        raise click.Abort

    return False


def inside_app_directory(ctx, exit_on_error=False):
    app_files = ['apps.py']

    for file in app_files:
        if ctx.obj['project_files'].get(file, None):
            return True

    Logger.error('Not inside an app directory')
    if exit_on_error:
        raise click.Abort

    return False


def wrong_place_warning(ctx):
    try:
        if (ctx.obj['path'] and ctx.obj['project']) is None:
            Logger.log('PROJECT_DIRECTORY_NOT_FOUND_ERROR')
            Logger.log('')
            Logger.log('PROJECT_DIRECTORY_NOT_FOUND_ERROR_HELP')
            raise click.Abort
    except (AttributeError, KeyError) as e:
        raise click.Abort


def not_in_project_warning():
    if '--help' in click.get_os_args():
        pass
    else:
        path, management, file = find_project_files(os.getcwd())
        if not management:
            Logger.log('PROJECT_DIRECTORY_NOT_FOUND_ERROR')
            raise click.Abort


def ensure_directory(d):
    try:
        os.listdir(d)
    except FileNotFoundError:
        os.makedirs(d)
