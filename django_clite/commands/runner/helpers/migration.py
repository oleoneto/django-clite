import os
import subprocess
from .runner import RunnerHelper


DEFAULT_MAKE_MIGRATIONS_COMMAND = ['python3', 'manage.py', 'makemigrations']

DEFAULT_MIGRATE_COMMAND = ['python3', 'manage.py', 'migrate']


class MigrationHelper(RunnerHelper):

    @classmethod
    def make_migrations(cls, path, app, options):
        os.chdir(path)

        if app is not None:
            DEFAULT_MAKE_MIGRATIONS_COMMAND.append(app)

        if options:
            for option in options:
                DEFAULT_MAKE_MIGRATIONS_COMMAND.append(option)

        subprocess.check_output(DEFAULT_MAKE_MIGRATIONS_COMMAND)

    @classmethod
    def migrate(cls, path, app, options):
        os.chdir(path)

        if app is not None:
            DEFAULT_MIGRATE_COMMAND.append(app)

        if options:
            for option in options:
                DEFAULT_MIGRATE_COMMAND.append(option)

        subprocess.check_output(DEFAULT_MIGRATE_COMMAND)

    @classmethod
    def run(cls, path, app, options):
        if app:
            cls.make_migrations(path, app, options)
            cls.migrate(path, app, options=options)
        else:
            cls.make_migrations(path, app=None, options=options)
            cls.migrate(path, app=None, options=options)
