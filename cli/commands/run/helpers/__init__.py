# cli:commands:run:helpers
import os
import re
import subprocess
from cli.logger import logger


DEFAULT_RUNSERVER_PLUS_COMMAND = ['python3', 'manage.py', 'runserver_plus', '8000']

DEFAULT_RUNSERVER_COMMAND = ['python3', 'manage.py', 'runserver', '8000']

DEFAULT_PROCESS_SUBGROUP = 'django-run-server-group-soliloquy'

BUILD_COMMAND = ['docker-compose', 'build']

START_COMMAND = ['docker-compose', 'up']


def make_migrations(path, app, options):
    os.chdir(path)

    try:
        management = os.path.join(path, 'manage.py')
        command = ['python3', management, 'makemigrations']
        if app is not None:
            command.append(app)

        # FIXME: determine how to handle manage.py flags or whether we should support them, at all.
        # for option in options:
        #     command.append(option)

        subprocess.check_call(command)
    except subprocess.CalledProcessError:
        pass


def migrate(path, app, options):
    os.chdir(path)

    try:
        management = os.path.join(path, 'manage.py')
        command = ['python3', management, 'migrate']
        if app is not None:
            command.append(app)

        # FIXME: determine how to handle manage.py flags or whether we should support them, at all.
        # for option in options:
        #     command.append(option)
        subprocess.check_call(command)
    except subprocess.CalledProcessError:
        pass


def __read_environment(env_file):
    """
    Use this to read environment variables from a .env file

    Based on implementations found on the links below:
        https://gist.github.com/bennylope/2999704
        https://wellfire.co/learn/easier-12-factor-django/
    """

    try:
        with open(env_file) as f:
            content = f.read()
    except IOError:
        content = ''

    keys = {}

    for line in content.splitlines():
        first_match = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if first_match:
            key, value = first_match.group(1), first_match.group(2)
            second_match = re.match(r"\A'(.*)'\Z", value)
            if second_match:
                value = second_match.group(1)
            third_match = re.match(r'\A"(.*)"\Z', value)
            if third_match:
                value = re.sub(r'\\(.)', r'\1', third_match.group(1))
            keys[key] = value

    return keys


def __copy_env(env_file, destination, project_name=None, dokku=True):
    keys = __read_environment(env_file)

    options = ['.env-dokku', '.env-example']

    output = options[0] if dokku else options[1]

    f = os.path.join(destination, output)

    with open(f, 'w') as file:
        for k, v in keys.items():
            if dokku:
                v = v.split("#")[0]
                if v not in ['False', 'True']:
                    v = f"'{v}'"
                statement = f"dokku config:set --no-restart {project_name} {k}={v}\n"
            else:
                statement = f'{k}=\n'
            file.write(statement)


def copy_dokku(env_file, destination, project_name):
    __copy_env(env_file, destination, project_name)
    logger.log('Exported environment to .env-dokku')


def copy_example(env_file, destination):
    __copy_env(env_file, destination, dokku=False)
    logger.log('Exported environment to .env-example')


# ...


def run_server(**kwargs):
    """
    Starts the default Django development server.
    """

    os.chdir(kwargs.get('cwd', os.getcwd()))

    port = kwargs.get('port', None)
    plus = kwargs.get('plus', None)

    if port:
        DEFAULT_RUNSERVER_PLUS_COMMAND[-1] = str(port)
        DEFAULT_RUNSERVER_COMMAND[-1] = str(port)

    try:
        if plus:
            subprocess.call(DEFAULT_RUNSERVER_PLUS_COMMAND)
        else:
            subprocess.call(DEFAULT_RUNSERVER_COMMAND)
    except subprocess.CalledProcessError:
        pass


def run_copy_environment(**kwargs):
    project_name = kwargs['project_name']

    if kwargs.get('filepath', None):
        env_file = kwargs.get('filepath')
    else:
        env_file = kwargs.get('path').joinpath('.env')

    try:
        f = open(env_file)
        f.close()
    except FileNotFoundError:
        logger.error("No environment file found.")
        raise

    destination = kwargs['destination']

    if kwargs['no_dokku'] and kwargs['no_example']:
        logger.error('Nothing to export. Skipping...')
        raise

    if not kwargs['no_example']:
        copy_example(env_file, destination)
    if not kwargs['no_dokku']:
        copy_dokku(env_file, destination, project_name)
