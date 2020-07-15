import click
import os
import subprocess
from .runner import RunnerHelper
from django.core.exceptions import ImproperlyConfigured

DEFAULT_MIGRATIONS_COMMAND = ['python3', 'manage.py', 'makemigrations']

DEFAULT_LOAD_COMMAND = ['python3', 'manage.py', 'loaddata']

DEFAULT_COLLECT_COMMAND = ['python3', 'manage.py', 'collectstatic', '--no-input']


class BuildHelper(RunnerHelper):

    def start(self, path, options=None):
        """
        Runs migrations, loads fixtures, and collects static files.
        """
        os.chdir(path)

        if options is not None:
            click.echo('Options passed...')

        try:
            # res = subprocess.check_call(DEFAULT_MIGRATIONS_COMMAND)
            # res = subprocess.call(DEFAULT_LOAD_COMMAND)
            res = subprocess.check_output(DEFAULT_COLLECT_COMMAND)
        except subprocess.CalledProcessError:
            click.Abort()
