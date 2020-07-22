import click
import os
import subprocess
from cli.helpers.logger import *
from cli.helpers import FSHelper
from cli.helpers import sanitized_string
from cli.helpers import rendered_file_template
from cli.helpers.errors import DEFAULT_ERRORS
from cli.helpers.errors import PROJECT_CREATION_ERROR
from cli.decorators import watch_templates
from cli.commands.create.helpers.app import AppHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

CURRENT_WORKING_DIRECTORY = '.'

PREVIOUS_WORKING_DIRECTORY = '..'

SETTINGS = {
    'settings.py': 'settings.tpl'
}

CLI_TEMPLATES = {
    '.config.json': 'cli-config_json.tpl',
}

DOCKER_TEMPLATES = {
    'Dockerfile': 'dockerfile.tpl',
    'docker-compose.yml': 'docker-compose.tpl',
    'docker-entrypoint.sh': 'docker-entrypoint.tpl',
}

DOKKU_TEMPLATES = {
    'app.json': 'app_json.tpl',
    'CHECKS': 'dokku_checks.tpl',
    'DOKKU_SCALE': 'dokku_scale.tpl',
    'Procfile': 'procfile.tpl',
}

HEROKU_TEMPLATES = {
    'Procfile': 'procfile.tpl',
    'requirements.txt': 'requirements.tpl',
}

ENV_TEMPLATES = {
    '.env': 'env.tpl',
    '.env-example': 'env.tpl',
}

GIT_TEMPLATES = {
    'README.md': 'README.tpl',
    '.gitignore': 'gitignore.tpl',
}

CELERY_TEMPLATES = {
    '__init__.py': 'celery.tpl',
    'tasks.py': 'celery_tasks.tpl',
}

STORAGES_TEMPLATES = {
    'storage.py': 'storage.tpl',
}

SETTINGS_TEMPLATES = {
    'settings.py': 'settings.tpl',
}


@watch_templates(os.path.join(BASE_DIR, 'templates/project'))
class CreatorHelper(FSHelper):
    """
    Creator Helper

    Aids the creation of projects and apps.
    Class has access to file system through FSHelper.
    """

    def __init__(self, cwd, dry=False, force=False, default=False, verbose=False):
        self.app_helper = AppHelper(cwd=cwd, dry=dry, force=force, default=default, verbose=verbose)
        super(CreatorHelper, self).__init__(cwd, dry, force, default, verbose)

    def __celery(self, project):
        """
        Add celery configurations to the project
        :param project: name of django project
        :return: directory of celery configurations
        """
        self.change_directory(project)
        self.change_directory(project)

        directory = os.getcwd()

        try:
            self.parse_templates(
                parings={'__init__.py': 'celery_init.tpl'},
                names=self.TEMPLATE_FILES,
                directory=self.TEMPLATES_DIRECTORY,
                force=True,
                context={'project': project}
            )

            self.change_directory(PREVIOUS_WORKING_DIRECTORY)
            self.change_directory(PREVIOUS_WORKING_DIRECTORY)
        except Exception as e:
            log_error(e)

        return directory

    def __git(self, project, origin):
        """
        :param project: name of django project
        :param origin: origin url of version control server
        :return: True if creation of repository is successful
        """
        self.change_directory(project)

        if self.is_dry:
            if self.verbose:
                log_standard("Skipping initialization of remote origin")
            return False

        self.create_repository()
        subprocess.check_output(['git', 'remote', 'add', 'origin', origin])
        log_success(f'Successfully added origin {origin}')

        # Return to top of project directory
        self.change_directory(PREVIOUS_WORKING_DIRECTORY)
        return True

    def __project(self, project, presets=None, **kwargs):
        """
        Creates a django project with or without customizations

        :param project: django project name
        :param presets: default options for django project
        :return: None
        """

        directory = None

        if presets is None:
            presets = []

        project = sanitized_string(project)

        supported_presets = {
            'celery': CELERY_TEMPLATES,
            'custom_settings': SETTINGS_TEMPLATES,
            'custom_storage': STORAGES_TEMPLATES,
            'dockerized': DOCKER_TEMPLATES,
            'dokku': DOKKU_TEMPLATES,
            'environments': ENV_TEMPLATES,
            'git': GIT_TEMPLATES,
            'heroku': HEROKU_TEMPLATES,
        }

        if self.is_dry:
            if self.verbose:
                log_standard("Skipping creation of project with --dry enabled")
            return

        # Generating project directory with the help of `django-admin`
        try:
            log_verbose(header=f'Attempting to create project: {project}')
            subprocess.check_output([
                'django-admin',
                'startproject',
                project
            ])
            try:
                # Parse templates
                self.parse_templates(
                    parings=CLI_TEMPLATES,
                    names=self.TEMPLATE_FILES,
                    directory=self.TEMPLATES_DIRECTORY,
                    force=True,
                    context={
                        'project': project,
                        'timeout': 60,
                        'wait': 20,
                        'web': 1,
                        **kwargs
                    }
                )
            except (KeyError, TypeError) as e:
                log_error(PROJECT_CREATION_ERROR)
        except subprocess.CalledProcessError:
            log_error(DEFAULT_ERRORS['project'])
            raise click.Abort

        if presets:
            # Customize django project directory
            self.change_directory(project)
            directory = os.getcwd()

            for preset in presets:
                depth = 0

                if preset == 'celery':
                    self.change_directory(project)
                    self.create_package(project=project, package='celery')
                    self.change_directory('celery')
                    depth += 2

                if preset in ['custom_settings', 'custom_storage']:
                    self.change_directory(project)
                    depth += 1

                try:
                    # Parse templates
                    self.parse_templates(
                        parings=supported_presets[preset],
                        names=self.TEMPLATE_FILES,
                        directory=self.TEMPLATES_DIRECTORY,
                        force=True,
                        context={
                            'project': project,
                            'timeout': 60,
                            'wait': 20,
                            'web': 1,
                            **kwargs
                        }
                    )
    
                    for d in range(depth):
                        self.change_directory(PREVIOUS_WORKING_DIRECTORY)
                except Exception as e:
                    log_error(e)

            # Return to top of project directory
            self.change_directory(PREVIOUS_WORKING_DIRECTORY)

        return directory

    def create_project(self, project, apps, presets, **kwargs):
        """
        Creates a project structure and customizes it

        :param project: name of django projects
        :param apps: project apps
        :param presets: list of project defaults/presets
        :param kwargs: extra options
        :return: path to project directory
        """

        # Create project
        directory = self.__project(project, presets, **kwargs)

        # Add customizations for celery
        if 'celery' in presets:
            self.__celery(project)

        # Add apps to django project
        if apps:
            for app in apps:
                self.change_directory(project)
                self.change_directory(project)

                self.app_helper.create_app(app=app, project=project)

                self.change_directory(PREVIOUS_WORKING_DIRECTORY)
                self.change_directory(PREVIOUS_WORKING_DIRECTORY)

        # Add special apps to django project
        if kwargs.get('custom_apps'):
            for app in kwargs.get('custom_apps'):
                auth = app == 'authentication'
                active_record = app == 'active_record'

                self.change_directory(project)
                self.change_directory(project)

                self.app_helper.create_app(
                    app=app,
                    auth=auth,
                    project=project,
                    active_record=active_record
                )

                self.change_directory(PREVIOUS_WORKING_DIRECTORY)
                self.change_directory(PREVIOUS_WORKING_DIRECTORY)

        # Create git repository
        if 'git' in presets:
            self.__git(project, origin=kwargs.get('origin'))

        return directory

    def create_file_in_context(self, project, template, filename, apps=None):
        """
        Creates a file in the context of the current project

        :param project:
        :param template:
        :param filename:
        :param apps:
        :return:
        """
        content = rendered_file_template(
            path=self.TEMPLATES_DIR,
            template=template,
            context={'project': project, 'apps': apps}
        )

        return self.create_file(
            content=content,
            filename=filename,
        )
