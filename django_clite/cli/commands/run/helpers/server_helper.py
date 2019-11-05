import os
import subprocess
from .base_run_helper import BaseRunHelper

DEFAULT_RUNSERVER_COMMAND = ['python3', 'manage.py', 'runserver', '8000']

DEFAULT_PROCESS_SUBGROUP = 'django-run-server-group-soliloquy'


class ServerHelper(BaseRunHelper):

    @classmethod
    def run(cls, **kwargs):
        """
        Starts the default Django development server.
        """
        os.chdir(kwargs['path'])

        try:
            DEFAULT_RUNSERVER_COMMAND[-1] = str(kwargs['port']) if kwargs['port'] else DEFAULT_RUNSERVER_COMMAND[-1]
        except KeyError:
            pass

        subprocess.call(DEFAULT_RUNSERVER_COMMAND)
