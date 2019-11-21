import os
import subprocess
from .runner import RunnerHelper

DEFAULT_RUNSERVER_COMMAND = ['python3', 'manage.py', 'runserver', '8000']

DEFAULT_PROCESS_SUBGROUP = 'django-run-server-group-soliloquy'


class ServerHelper(RunnerHelper):

    def run(self, **kwargs):
        """
        Starts the default Django development server.
        """
        os.chdir(self.cwd)

        try:
            DEFAULT_RUNSERVER_COMMAND[-1] = str(kwargs['port']) \
                if kwargs['port'] \
                else DEFAULT_RUNSERVER_COMMAND[-1]
        except KeyError:
            pass

        subprocess.call(DEFAULT_RUNSERVER_COMMAND)
