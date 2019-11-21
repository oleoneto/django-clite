# helpers
import os
import re
import sys
import fileinput
from .logger import *
from .parser import sanitized_string
from .templates import rendered_file_template
from .fs import FSHelper


def find_project_files(cwd):
    """
    Searches the current working directory for any of 4 key Django files:
    manage.py, settings.py, wsgi.py, and apps.py to determine from where a command
    is being run. This is used to ensure commands that create or delete resources
    are always run in the correct directory and within a Django project.
    """
    code = 0
    path = None
    management = None
    file = None

    levels = (
        ('manage.py', 1),    # <-- project
        ('settings.py', 2),  # <-- project/project
        ('wsgi.py', 2),      # <-- project/project
        ('apps.py', 3),      # <-- project/project/app
    )

    for filename, c in levels:
        if filename in os.listdir(cwd):
            code = c
            path = cwd

    if code == 1:
        management = path
        path = f"{path}/{path.split('/')[-1]}"
        file = os.path.join(management, 'manage.py')
    elif code == 2:
        management = path.rsplit('/', 1)[0]
        file = os.path.join(management, 'manage.py')
    elif code == 3:
        management = path.rsplit('/', 2)[0]
        path = path.rsplit('/', 1)[0]
        file = os.path.join(management, 'manage.py')
    return path, management, file


def find_settings_file(path):
    settings = os.path.join(path, 'settings.py')
    if not os.path.exists(settings):
        raise FileNotFoundError(
            "Can't find `settings.py` file: "f"{settings}"
        )
    return settings


def get_app_name(path='.', find_first=False):
    """
    Searches current directory for apps.py in order to
    retrieve the application name from it.
    """

    if find_first:
        p, m, f = find_project_files(path)
        management_file = f

    try:
        for line in fileinput.input('apps.py'):
            if "name = " in line:
                fileinput.close()
                return line.split(" = ")[1].lstrip().replace("\n", "").replace("'", "")
        fileinput.close()
    except FileNotFoundError:
        return "app"
    return "app"


def get_project_name(management_file=None, find_first=False):
    if find_first:
        p, m, f = find_project_files('.')
        management_file = f

    with open(management_file, 'r') as file:
        for line in file:
            if 'DJANGO_SETTINGS_MODULE' in line:
                line = line.\
                    replace("'", "").\
                    replace(" ", "").\
                    split(',')[-1].\
                    split('.')[0]
                return line
    return None


def replace_line(value, parameter_name, settings_file):
    """
    Based on implementation from djecrety
    https://github.com/mrouhi13/djecrety/blob/master/djecrety/utils.py
    """

    parameter_is_exist = False
    if parameter_name:
        new_line = f'{parameter_name} = {value}'
        line_pattern = fr'^{parameter_name} = .*'

        for line in fileinput.input(settings_file, inplace=True):
            if re.match(line_pattern, line):
                parameter_is_exist = True
                line = re.sub(line_pattern, new_line, line)
            sys.stdout.write(line)

        if not parameter_is_exist:
            raise NameError(f"Can't find parameter name: {parameter_name}")
        return True
    return False


def save_to_settings(value, parameter, path):
    """
    Save the value to the given parameter in `settings.py` file.
    """
    settings = find_settings_file(path)

    return replace_line(value, parameter, settings)
