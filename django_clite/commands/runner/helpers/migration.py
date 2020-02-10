import os
import subprocess
from .runner import RunnerHelper
from django_clite.helpers.logger import log_error


class MigrationHelper(RunnerHelper):

    @classmethod
    def make_migrations(cls, path, app, options):
        os.chdir(path)

        try:
            management = os.path.join(path, 'manage.py')
            command = ['python3', management, 'makemigrations']
            if app is not None:
                command.append(app)
            # TODO: determine how to handle manage.py flags
            #   or whether we should support them, at all.
            # for option in options:
            #     command.append(option)
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            pass

    @classmethod
    def migrate(cls, path, app, options):
        os.chdir(path)

        try:
            management = os.path.join(path, 'manage.py')
            command = ['python3', management, 'migrate']
            if app is not None:
                command.append(app)
            # TODO: determine how to handle manage.py flags
            #   or whether we should support them, at all.
            # for option in options:
            #     command.append(option)
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            pass

    @classmethod
    def run(cls, path, app, options):
        if app:
            cls.make_migrations(path, app, options)
            cls.migrate(path, app, options=options)
        else:
            cls.make_migrations(path, app=None, options=options)
            cls.migrate(path, app=None, options=options)
