import click
import os
import subprocess

DEFAULT_RUNSERVER_COMMAND = ['python3', 'manage.py', 'runserver', '8000']

DEFAULT_RUNSERVER_PLUS_COMMAND = ['python3', 'manage.py', 'runserver_plus']

DEFAULT_PROCESS_SUBGROUP = 'django-run-server-group-soliloquy'


class ServerHelper(object):

    @classmethod
    def start(cls, path, port):
        """
        Starts the default Django development server.
        """
        os.chdir(path)

        if port is not None:
            DEFAULT_RUNSERVER_COMMAND[-1] = str(port)

        subprocess.call(DEFAULT_RUNSERVER_COMMAND)
