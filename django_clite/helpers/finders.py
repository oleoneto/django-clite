import os
import re
import sys
from os import path
import fileinput
from .logger import log_info


def walk_up(directory_path):
    """
    Implementation by Michele Pasin
    https://gist.github.com/zdavkeos/1098474#gistcomment-2943865

    Mimic os.walk, but walk 'up' instead of down the directory tree.
    """

    directory_path = path.realpath(directory_path)

    # get files in current dir
    try:
        names = os.listdir(directory_path)
    except Exception as e:
        print(e)
        return

    dirs, non_dirs = [], []
    for name in names:
        if path.isdir(path.join(directory_path, name)):
            dirs.append(name)
        else:
            non_dirs.append(name)

    yield directory_path, dirs, non_dirs

    new_path = path.realpath(path.join(directory_path, '..'))

    # see if we are at the top
    if new_path == directory_path:
        return

    for x in walk_up(new_path):
        yield x


def find_project_files(cwd):
    """
    Searches the current working directory for any of 4 key Django files:
    manage.py, settings.py, wsgi.py, and apps.py to determine from where a command
    is being run. This is used to ensure commands that create or delete resources
    are always run in the correct directory and within a Django project.
    """

    code = 0
    path = None
    project_directory = None
    management_file = None

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
        project_directory = path
        management_file = os.path.join(project_directory, 'manage.py')

    elif code == 2 or code == 3:
        for c, d, f in walk_up('.'):
            if 'manage.py' in f:
                project_directory = c
                management_file = os.path.join(project_directory, 'manage.py')
                break

    return path, project_directory, management_file


def find_settings_file(path):
    settings = os.path.join(path, 'settings.py')
    if not os.path.exists(settings):
        raise FileNotFoundError(
            "Can't find `settings.py` file: "f"{settings}"
        )
    return settings


def get_project_name(management_file=None, find_first=False):
    if find_first:
        p, m, f = find_project_files('.')
        management_file = f

    try:
        with open(management_file, 'r') as file:
            for line in file:
                if 'DJANGO_SETTINGS_MODULE' in line:
                    line = line.\
                        replace("'", "").\
                        replace(" ", "").\
                        replace('"', "").\
                        split(',')[-1].\
                        split('.')[0]
                    return line
    except TypeError:
        pass
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


def get_app_name(*args, **kwargs):
    """
    Searches current directory for apps.py in order to
    retrieve the application name from it.
    """

    # Assume cwd is *app/models
    # walk up from the directory in search for apps.py and AppConfig
    base = None

    if kwargs.get('verbose'):
        log_info(f"Searching for AppConfig at {os.getcwd()}")

    for root, dirs, files in walk_up(os.getcwd()):
        if "apps.py" in files:
            base = root

    if not base:
        if kwargs.get('verbose'):
            log_info(f"Cannot find for AppConfig for this app.")

        return "app"

    os.chdir(base)

    try:
        for line in fileinput.input('apps.py'):
            if "name = " in line:
                fileinput.close()
                return line.split(" = ")[-1] \
                    .lstrip() \
                    .replace("\n", "") \
                    .replace("'", "") \
                    .split('.')[-1]
        fileinput.close()
    except FileNotFoundError:
        pass

    os.chdir(PREVIOUS_WORKING_DIRECTORY)
    return "app"
