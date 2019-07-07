import os
import subprocess
import sys
from djangle.cli import log_error, log_info, log_success, sanitized_string
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.git_repo.readme import readme_template
from djangle.cli.templates.git_repo.gitignore import git_ignore_template
from djangle.cli.templates.router import router_template
from djangle.cli.templates.urls import app_urls_template
from djangle.cli.templates.env import env_template
from djangle.cli.templates.requirements import (
    requirements_template,
    pipenv_template
)
from djangle.cli.templates.docker import (
    docker_compose_template,
    dockerfile_template
)
from djangle.cli.templates.dokku import (
    app_template,
    dokku_checks_template,
    dokku_scale_template,
    procfile_template
)


DEFAULT_ERRORS = {
    "project": "Unable to create project. Will exit.",
    "app": "Unable to create app. Skipping...",
    "clean": "Unable to remove default files. Skipping...",
    "repo": "Unable to initialize repository. Skipping...",
    "touch": "Unable to create default files. Skipping...",
}

DEFAULT_APP_PACKAGES = {
    'admin', 'forms', 'models', 'serializers',
    'templates', 'tests', 'views', 'viewsets'
}

DEFAULT_CWD = '.'

DEFAULT_PREVIOUS_WD = '..'


class CreatorHelper(object):

    helper = BaseHelper()

    @classmethod
    def create_app(cls, **kwargs):
        """
        Creates an app and its respective packages
        """
        project_name = sanitized_string(kwargs['project'])
        app_name = sanitized_string(kwargs['app_name'])

        # Create application structure
        try:
            subprocess.check_output(['django-admin', 'startapp', app_name])
        except subprocess.CalledProcessError:
            log_error(DEFAULT_ERRORS['app'])
            return

        # Enter app directory
        os.chdir(app_name)

        # Remove unused modules
        try:
            subprocess.check_output(['rm', 'admin.py', 'models.py', 'tests.py', 'views.py', '__init__.py'])
        except subprocess.CalledProcessError:
            log_error(DEFAULT_ERRORS['clean'])

        # Add urls.py module
        try:
            cls.helper.parse_and_create(
                template=app_urls_template,
                project=project_name,
                app_name=app_name,
                filename='urls.py',
                path=DEFAULT_CWD
            )
            cls.helper.create_file(
                path=DEFAULT_CWD,
                filename='__init__.py',
                file_content=f'# application:{app_name}'
            )
        except subprocess.CalledProcessError:
            log_error(DEFAULT_ERRORS['touch'])

        # Add packages to app structure
        for package in DEFAULT_APP_PACKAGES:
            cls.create_app_package(package_name=package, app_name=app_name)
            os.chdir(DEFAULT_PREVIOUS_WD)

        os.chdir(DEFAULT_PREVIOUS_WD)
        log_success(f'Successfully created application: {app_name}')

    @classmethod
    def create_app_package(cls, **kwargs):
        """
        Create an app package and any associated sub-packages or modules
        """
        app_name = sanitized_string(kwargs['app_name'])
        package_name = sanitized_string(kwargs['package_name'])
        cls.create_package(package_name=package_name, app_name=app_name)

        # Do customizations
        os.chdir(package_name)
        cls.create_package(package_name='helpers', app_name=app_name)
        if package_name == 'admin':
            cls.create_package(package_name='actions', app_name=app_name)
            cls.create_package(package_name='inlines', app_name=app_name)
            cls.create_package(package_name='permissions', app_name=app_name)
        if package_name == 'models':
            cls.create_package(package_name='managers', app_name=app_name)
            cls.create_package(package_name='validators', app_name=app_name)
            cls.create_package(package_name='signals', app_name=app_name)
        if package_name == 'viewsets':
            cls.helper.parse_and_create(
                template=router_template,
                app_name=app_name,
                filename='router.py',
                path=DEFAULT_CWD
            )

    @classmethod
    def create_package(cls, **kwargs):
        """
        Create a package and any associated modules
        """
        app_name = sanitized_string(kwargs['app_name'])
        package_name = sanitized_string(kwargs['package_name'])
        content = f'# {app_name}:{package_name}'

        os.mkdir(package_name)
        os.chdir(package_name)
        cls.helper.create_file(path=DEFAULT_CWD, filename='__init__.py', file_content=content)
        os.chdir(DEFAULT_PREVIOUS_WD)

    @classmethod
    def create_project(cls, **kwargs):
        """
        Creates a project structure and its dependent packages
        """

        project_name = sanitized_string(kwargs['project'])

        # Creating project
        try:
            log_info(f"Attempting to create project: {project_name}...")
            subprocess.check_output(['django-admin', 'startproject', project_name])
        except subprocess.CalledProcessError:
            log_error(DEFAULT_ERRORS['project'])
            sys.exit(-1)

        # Add customizations
        os.chdir(project_name)

        cls.handle_docs_and_misc(**kwargs)

        cls.handle_dependencies(**kwargs)

        if kwargs['dokku']:
            cls.handle_dokku(**kwargs)

        if kwargs['docker']:
            cls.handle_docker(**kwargs)

        # Inside project/project/
        os.chdir(project_name)

        if kwargs['custom_auth']:
            cls.handle_custom_auth(**kwargs)

        if kwargs['apps']:
            for app in kwargs['apps']:
                cls.create_app(app_name=app, **kwargs)

        # cd ../../
        os.chdir(DEFAULT_PREVIOUS_WD)

        try:
            cls.handle_git()
        except subprocess.CalledProcessError:
            log_error(DEFAULT_ERRORS['repo'])

        log_success(f"Created project: {kwargs['project']}")

    @classmethod
    def handle_custom_auth(cls, **kwargs):
        app_name = 'authentication'
        cls.create_app(app_name=app_name, project=kwargs['project'])
        os.chdir(app_name)
        # TODO: Add configurations to settings.py
        os.chdir(DEFAULT_PREVIOUS_WD)
        log_success('Created authentication app for custom auth')

    @classmethod
    def handle_dokku(cls, **kwargs):
        try:
            project_name = sanitized_string(kwargs['project'])

            os.mkdir('dokku')
            os.chdir('dokku')

            # app.json
            cls.helper.parse_and_create(
                template=app_template,
                project=project_name,
                filename='app.json',
                path=DEFAULT_CWD
            )

            # Procfile
            cls.helper.parse_and_create(
                template=procfile_template,
                project=project_name,
                filename='Procfile',
                path=DEFAULT_CWD
            )

            # CHECKS
            cls.helper.parse_and_create(
                template=dokku_checks_template,
                project=project_name,
                filename='CHECKS',
                wait=20,
                timeout=60,
                path=DEFAULT_CWD
            )

            cls.helper.parse_and_create(
                template=dokku_checks_template,
                project=project_name,
                filename='CHECKS',
                wait=20,
                timeout=60,
                path=DEFAULT_PREVIOUS_WD
            )

            # DOKKU_SCALE
            cls.helper.parse_and_create(
                template=dokku_scale_template,
                project=project_name,
                filename='DOKKU_SCALE',
                web=1,
                path=DEFAULT_CWD
            )

            os.chdir(DEFAULT_PREVIOUS_WD)
        except subprocess.CalledProcessError:
            log_error(DEFAULT_ERRORS['touch'])

    @classmethod
    def handle_docker(cls, **kwargs):
        project_name = sanitized_string(kwargs['project'])

        # docker-compose
        cls.helper.parse_and_create(
            template=docker_compose_template,
            project=project_name,
            filename='docker-compose.yml',
            path=DEFAULT_CWD
        )

        # Dockerfile
        cls.helper.parse_and_create(
            template=dockerfile_template,
            project=project_name,
            filename='Dockerfile',
            path=project_name
        )

    @classmethod
    def handle_dependencies(cls, **kwargs):
        project_name = sanitized_string(kwargs['project'])

        # Pipfile
        cls.helper.parse_and_create(
            template=pipenv_template,
            project=project_name,
            filename='Pipfile',
            path=DEFAULT_CWD,
        )

        # Requirements
        cls.helper.parse_and_create(
            template=requirements_template,
            project=project_name,
            filename='requirements.txt',
            path=DEFAULT_CWD
        )

    @classmethod
    def handle_docs_and_misc(cls, **kwargs):
        project_name = sanitized_string(kwargs['project'])

        # README
        cls.helper.parse_and_create(
            template=readme_template,
            project=project_name,
            filename='README.md',
            path=DEFAULT_CWD
        )

        # Git Ignore
        cls.helper.parse_and_create(
            template=git_ignore_template,
            project=project_name,
            filename='.gitignore',
            path=DEFAULT_CWD
        )

        # Environment files
        cls.helper.parse_and_create(
            path=DEFAULT_CWD,
            filename='.env',
            template=env_template
        )

        cls.helper.parse_and_create(
            path=DEFAULT_CWD,
            filename='.env-example',
            template=env_template
        )

    @classmethod
    def handle_git(cls):
        subprocess.check_output(['git', 'init'])
        subprocess.check_output(['git', 'add', '--all'])
        subprocess.check_output(['git', 'commit', '-m', 'Initial commit'])
        log_success('Successfully initialized git repository')
# end class
