from djangle.cli import log_error, log_info, log_success
import os
import shutil
import subprocess
import sys
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.requirements import requirements_template
from djangle.cli.templates.git_repo.readme import readme_template
from djangle.cli.templates.git_repo.gitignore import git_ignore_template
from djangle.cli.templates.router import router_template
from djangle.cli.templates.urls import app_urls_template
from djangle.cli.templates.docker import docker_compose_template, dockerfile_template
from djangle.cli.templates.dokku import (
    app_template,
    dokku_checks_template,
    dokku_scale_template,
    procfile_template
)


DEFAULT_ERROR = {
                "project": "Unable to create project. Will exit with code: ",
                "app": "Unable to create app. Skipping...",
                "clean": "Unable to remove default files. Skipping...",
                "repo": "Unable to initialize repository. Skipping...",
                "touch": "Unable to create default files. Skipping...",
            }


class CreatorHelper(object):
    def create(self, **kwargs):
        if 'project' in kwargs.keys():
            try:
                self.__create_project(**kwargs)
                return
            except subprocess.CalledProcessError as error:
                log_error(DEFAULT_ERROR['project'])
                log_error(error.output)
                sys.exit(-1)
        if 'apps' in kwargs.keys():
            self.__create_app(**kwargs)
    # end def

    def __create_app(self, **kwargs):

        helper = BaseHelper()

        for app_name in kwargs['apps']:
            log_info(f"Creating application...")

            # Handle creation of each app with django-admin
            try:
                subprocess.check_output(['django-admin', 'startapp', app_name])
            except subprocess.CalledProcessError as error:
                log_error(DEFAULT_ERROR['app'])
                log_error(error.output)

            # Run cli-specific configuration
            # ---------------------------------------------------
            os.chdir(app_name)

            try:
                # Remove unnecessary files (these will be replaced with packages)
                subprocess.check_output(['rm', 'models.py', 'views.py', 'tests.py', 'admin.py'])
            except subprocess.CalledProcessError as error:
                log_error(error.output)
                log_error(DEFAULT_ERROR['clean'])

            try:
                urls = helper.parse_template(template=app_urls_template)
                helper.create_file(path='.', filename='urls.py', file_content=urls)
            except subprocess.CalledProcessError as error:
                log_error(error.output)
                log_error(DEFAULT_ERROR['touch'])

            # Create app packages
            self.__create_app_packages(path='admin', app_name=app_name)
            self.__create_app_packages(path='forms', app_name=app_name)
            self.__create_app_packages(path='serializers', app_name=app_name)
            self.__create_app_packages(path='templates', app_name=app_name)
            self.__create_app_packages(path='tests', app_name=app_name)
            self.__create_app_packages(path='views', app_name=app_name)
            self.__create_app_packages(path='viewsets', app_name=app_name)
            self.__create_app_packages(path='models', app_name=app_name)

            # ---------------------------------------------------
            # Leave directory
            log_success(f"Created app: {app_name}")
            os.chdir('..')
    # end def

    def __create_project(self, **kwargs):
        try:
            log_info(f"Creating project...")

            try:
                # Create project with django-admin
                subprocess.check_output(['django-admin', 'startproject', kwargs['project']])
            except subprocess.CalledProcessError as error:
                log_error(error.output)
                log_error(DEFAULT_ERROR['project'])
                sys.exit(-1)

            # Run cli-specific configuration
            # Inside nested directory
            # ----------------------------------------
            os.chdir(kwargs['project'])

            # TODO: Create virtual environment

            # Default helper
            helper = BaseHelper()

            reqs = helper.parse_template(template=requirements_template, project=kwargs['project'])
            helper.create_file(path='.', filename='requirements_template.txt', file_content=reqs)

            # Handle creation of docker-compose and Dockerfile
            if kwargs['docker']:
                # Add content to docker-compose and requirements_template
                compose = helper.parse_template(template=docker_compose_template, project=kwargs['project'])
                helper.create_file(path='.', filename='docker-compose.yml', file_content=compose)

            # Handle creation of dokku directory and appropriate files
            if kwargs['dokku']:
                try:
                    os.mkdir('dokku')
                    os.chdir('dokku')

                    app = helper.parse_template(template=app_template)
                    helper.create_file(path='.', filename='app.json', file_content=app)

                    procfile = helper.parse_template(template=procfile_template, project=kwargs['project'])
                    helper.create_file(path='.', filename='Procfile', file_content=procfile)

                    checks = helper.parse_template(template=dokku_checks_template, wait=20, timeout=60)
                    helper.create_file(path='.', filename='CHECKS', file_content=checks)
                    helper.create_file(path='..', filename='CHECKS', file_content=checks)

                    scale = helper.parse_template(template=dokku_scale_template, web=1)
                    helper.create_file(path='.', filename='DOKKU_SCALE', file_content=scale)

                    os.chdir('..')
                except subprocess.CalledProcessError:
                    sys.exit(-1)

            # Get sub-directory, i.e. Project/Project/
            os.chdir(kwargs['project'])

            if kwargs['docker']:
                docker = helper.parse_template(template=dockerfile_template, project=kwargs['project'])
                helper.create_file(path='.', filename='Dockerfile', file_content=docker)

            if kwargs['core']:
                self.__create_app(apps=['core'])

                # TODO: Add configurations to settings.py

            try:
                self.__create_app(**kwargs)
            except KeyError:
                log_error(DEFAULT_ERROR['app'])

            # Leave directory
            os.chdir('..')

            # Initialize repository
            readme_file = helper.parse_template(template=readme_template, project=kwargs['project'])
            helper.create_file(path='.', filename='README.md', file_content=readme_file)

            gitignore_file = helper.parse_template(template=git_ignore_template)
            helper.create_file(path='.', filename='.gitignore', file_content=gitignore_file)

            try:
                c = subprocess.check_output(['git', 'init'])
                c = subprocess.check_output(['git', 'add', '--all'])
                c = subprocess.check_output(['git', 'commit', '-m', 'Initial commit'])
            except:
                log_error("Unable to proceed")
            log_success(f"Created project: {kwargs['project']}")

            return
        except KeyError:
            return
    # end def

    def __create_app_packages(self, **kwargs):

        app_name = kwargs['app_name']
        folder_name = kwargs['path']
        helper = BaseHelper()

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

            if folder_name == 'viewsets':
                router = helper.parse_template(template=router_template, app_name=app_name)
                helper.create_file(path='.', filename='router.py', file_content=router)

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
