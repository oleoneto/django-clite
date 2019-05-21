from djangocli.cli import log_error, log_info, log_success
import os
import shutil
import subprocess
from django.core.management.base import CommandError
from djangocli.cli.templates.docker import docker_compose as composeTemplate, dockerfile as DockerfileTemplate
from djangocli.cli.templates.requirements import requirements as requirementsTemplate
from djangocli.cli.templates.git_repo.readme import readmeTemplate
from djangocli.cli.templates.git_repo.gitignore import gitignoreTemplate
from djangocli.cli.commands.base_helper import BaseHelper


class CreatorHelper(object):
    def create(self, **kwargs):
        if 'project' in kwargs.keys():
            self.__create_project(**kwargs)
            return
        if 'apps' in kwargs.keys():
            self.__create_app(**kwargs)
    # end def

    def __create_app(self, **kwargs):

        for app_name in kwargs['apps']:
            log_info(f"Creating application...")

            # Handle creation of each app with django-admin
            try:
                subprocess.call(['django-admin', 'startapp', app_name])
            except CommandError:
                log_error("Error")

            # Run cli-specific configuration
            # ---------------------------------------------------
            os.chdir(app_name)

            # Remove unnecessary files (these will be replaced with packages)
            subprocess.call(['rm', 'models.py', 'views.py', 'tests.py', 'admin.py'])

            # Add app-specific urls configuration file
            subprocess.call(['touch', 'urls.py'])

            # Create app packages
            self.__create_app_packages(path='admin')
            self.__create_app_packages(path='forms')
            self.__create_app_packages(path='serializers')
            self.__create_app_packages(path='templates')
            self.__create_app_packages(path='tests')
            self.__create_app_packages(path='views')
            self.__create_app_packages(path='viewsets')
            self.__create_app_packages(path='models')

            # ---------------------------------------------------
            # Leave directory
            log_success(f"Created app: {app_name}")
            os.chdir('..')
    # end def

    def __create_project(self, **kwargs):
        try:
            log_info(f"Creating project...")

            # Create project with django-admin
            subprocess.call(['django-admin', 'startproject', kwargs['project']])

            # Run cli-specific configuration
            # Inside nested directory
            # ----------------------------------------
            os.chdir(kwargs['project'])

            # TODO: Create virtual environment

            # Default helper
            helper = BaseHelper()

            reqs = helper.parse_template(template=requirementsTemplate, project=kwargs['project'])
            helper.create_file(path='.', filename='requirements.txt', file_content=reqs)

            if kwargs['docker']:

                # Add content to docker-compose and requirements
                compose = helper.parse_template(template=composeTemplate, project=kwargs['project'])
                helper.create_file(path='.', filename='docker-compose.yml', file_content=compose)

            # Get sub-directory, i.e. Project/Project/
            os.chdir(kwargs['project'])

            if kwargs['docker']:
                docker = helper.parse_template(template=DockerfileTemplate, project=kwargs['project'])
                helper.create_file(path='.', filename='Dockerfile', file_content=docker)

            # TODO: Add configurations to settings.py
            # ...

            try:
                self.__create_app(**kwargs)
            except KeyError:
                pass

            # Leave directory
            os.chdir('..')

            # Initialize repository
            readme_file = helper.parse_template(template=readmeTemplate, project=kwargs['project'])
            helper.create_file(path='.', filename='README.md', file_content=readme_file)

            gitignore_file = helper.parse_template(template=gitignoreTemplate)
            helper.create_file(path='.', filename='.gitignore', file_content=gitignore_file)

            subprocess.call(['git', 'init'])
            subprocess.call(['git', 'add', '--all'])
            subprocess.call(['git', 'commit', '-m', 'Initial commit'])
            log_success(f"Created project: {kwargs['project']}")

            return
        except KeyError:
            return
    # end def

    def __create_app_packages(self, **kwargs):

        folder_name = kwargs['path']

        # Get location of this very file...
        __here__ = os.path.dirname(os.path.abspath(__file__))

        try:
            # Create main package
            self.__create_sub_package(path=folder_name)
            os.chdir(folder_name)

            self.__create_sub_package(path='helpers')

            # TODO: Fix: app packages being created inside /models
            # Create files for /models directory
            if folder_name == 'models':
                self.__create_sub_package(path='managers')
                self.__create_sub_package(path='signals')

                # Copy identifier.py to /helpers
                shutil.copyfile(f'{__here__}/identifier.py', 'helpers/identifier.py')

            if folder_name == 'admin':
                self.__create_sub_package(path='actions')
                self.__create_sub_package(path='inlines')
                self.__create_sub_package(path='permissions')

            os.chdir('..')
        except FileExistsError:
            return
    # end def

    def __create_sub_package(self, **kwargs):

        # __init__ message
        message = '# Import/register your modules here...\n'

        os.mkdir(kwargs['path'])
        os.chdir(kwargs['path'])
        with open('__init__.py', 'x') as file:
            file.write(message)
        os.chdir('..')
    # end def
# end class
