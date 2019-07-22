import os
import subprocess


DEFAULT_MAKE_MIGRATIONS_COMMAND = ['python3', 'manage.py', 'makemigrations']

DEFAULT_MIGRATE_COMMAND = ['python3', 'manage.py', 'migrate']


class MigrationHelper(object):

    @classmethod
    def make_migrations(cls, path, app):
        os.chdir(path)

        if app is not None:
            DEFAULT_MAKE_MIGRATIONS_COMMAND.append(app)

        command = DEFAULT_MAKE_MIGRATIONS_COMMAND

        subprocess.check_output(command)

    @classmethod
    def migrate(cls, path, app):
        os.chdir(path)

        if app is not None:
            DEFAULT_MIGRATE_COMMAND.append(app)

        command = DEFAULT_MIGRATE_COMMAND

        subprocess.check_output(command)

    @classmethod
    def run(cls, path, app, up, show):
        # cls.make_migrations(path, app)
        # cls.migrate(path, app)
        print(path)
        print(app)
        print(up)
        print(show)
