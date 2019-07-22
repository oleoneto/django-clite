# django-clite
import click
import inflection
import os


def file_created(filename=''):
    log_success("Successfully created %s" % filename)


def file_exists(filename=''):
    log_error("File already exists %s" % filename)


def find_management_file(cwd):
    """
    Searches the current working directory for any of 4 key Django files:
    manage.py, settings.py, wsgi.py, and apps.py to determine from where a command
    is being run. This is used to ensure commands that create or delete resources
    are always run in the correct directory and within a Django project.
    """
    code = 0
    path = None
    management = None

    levels = (
        ('manage.py', 1),    # <-- project
        ('settings.py', 2),  # <-- project/project
        ('wsgi.py', 2),      # <-- project/project
        ('apps.py', 3),      # <-- project/project/app
    )

    for filename, c in levels:
        if filename in os.listdir(cwd):
            code = c
            path = os.getcwd()

    if code == 1:
        management = path
        path = f"{path}/{path.split('/')[-1]}"
    elif code == 2:
        management = path.rsplit('/', 1)[0]
    elif code == 3:
        management = path.rsplit('/', 2)[0]
        path = path.rsplit('/', 1)[0]
    return path, management, code


def log_info(message):
    click.secho(message, fg='yellow')


def log_success(message):
    click.secho(message, fg='green')


def log_error(message):
    click.secho(message, fg='red')


def sanitized_string(text):
    """
    Ensures strings are properly sanitized and
    no special characters are present.
    """
    r = inflection.transliterate(text)
    r = r.replace(' ', '-')
    return inflection.underscore(r).lower()
