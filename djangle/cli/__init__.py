import click
import inflection
import os


class AliasedGroup(click.Group):
    """
    Adds support for abbreviated commands
    """
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


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
        path = f"{path}/{path.split('/')[-1]}"
    elif code == 3:
        path = f"{path.rsplit('/', 1)[0]}"
    return path, code


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
