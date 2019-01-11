from djangocli.cli import log_error, log_success
import os
import subprocess
from django.core.management.base import CommandError


class CreatorHelper():
    def create(self, *args, **kwargs):
        if 'project' in kwargs.keys():
            self.__create_project(**kwargs)
            return
        if 'apps' in kwargs.keys():
            self.__create_app(**kwargs)
    # end def

    # TODO: return each app directory
    def __create_app(self, *args, **kwargs):

        # Get directory of manage.py file
        __dir__ = self.__get_manage_py_dir()

        # ...
        if __dir__:
            if 'nested' in kwargs.keys():
                if kwargs['nested']:
                    os.chdir(__dir__.split('/')[-1])

        for app_name in kwargs['apps']:
            log_success(f"Creating application: {app_name}")

            # Handle creation of each app with django-admin
            try:
                subprocess.call(['django-admin', 'startapp', app_name])
            except CommandError:
                log_error("Error")

            # Run cli-specific configuration
            # os.chdir(app_name)

            # Leave directory
            # os.chdir('..')
    # end def

    # TODO: return project directory
    def __create_project(self, *args, **kwargs):
        try:
            log_success(f"Creating project: {kwargs['project']}")

            # Create project with django-admin
            subprocess.call(['django-admin', 'startproject', kwargs['project']])

            # Run cli-specific configuration
            # Inside nested directory
            os.chdir(kwargs['project'])
            os.chdir(kwargs['project'])

            # ...
            try:
                self.__create_app(**kwargs)
            except KeyError:
                pass

            # Leave directory
            os.chdir('..')
            print(os.getcwd())
            return
        except KeyError:
            return
    # end def

    def __get_manage_py_dir(self):
        # TODO: search directory for manage.py to determine nested directory

        if "manage.py" not in os.listdir():
            log_error("manage.py not found")
            return None

        return os.getcwd()
    # end def
# end class
