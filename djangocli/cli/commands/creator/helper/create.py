from djangocli.cli import log_error, log_info, log_success
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

        for app_name in kwargs['apps']:
            log_info(f"Creating application: {app_name}")

            # Handle creation of each app with django-admin
            try:
                subprocess.call(['django-admin', 'startapp', app_name])
            except CommandError:
                log_error("Error")

            # Run cli-specific configuration
            os.chdir(app_name)
            self.__create_app_packages('forms')
            self.__create_app_packages('models')
            self.__create_app_packages('serializers')
            self.__create_app_packages('templates')
            self.__create_app_packages('tests')
            self.__create_app_packages('views')
            self.__create_app_packages('viewsets')

            # Leave directory
            log_success(f"Created app: '{app_name}' inside {os.getcwd()}")
            os.chdir('..')
    # end def

    # TODO: return project directory
    def __create_project(self, *args, **kwargs):
        try:
            log_info(f"Creating project: {kwargs['project']}")

            # Create project with django-admin
            subprocess.call(['django-admin', 'startproject', kwargs['project']])

            # Run cli-specific configuration
            # Inside nested directory
            os.chdir(kwargs['project'])

            # Get current directory, i.e. Project/
            kwargs['__dir__'] = os.getcwd()

            # Get sub-directory, i.e. Project/Project/
            os.chdir(kwargs['project'])

            # ...
            try:
                self.__create_app(**kwargs)
            except KeyError:
                pass

            # Leave directory
            os.chdir('..')
            log_success(f"Created project: '{kwargs['project']}' inside {os.getcwd()}")
            return
        except KeyError:
            return
    # end def

    def __create_app_packages(self, folder_name):

        try:
            os.mkdir(folder_name)
            os.chdir(folder_name)
            with open('__ini__.py', 'x') as file:
                file.write('# Import modules here...\n')
            os.chdir('..')
        except FileExistsError:
            return
    # end def
# end class
