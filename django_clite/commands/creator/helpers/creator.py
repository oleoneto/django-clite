import os
import subprocess
import inflection
from enum import Enum, auto, unique
from django_clite.helpers.logger import *
from django_clite.helpers import FSHelper
from django_clite.helpers import sanitized_string
from django_clite.helpers import rendered_file_template
from django_clite.commands.generator.helpers import AdminHelper
from django_clite.commands.generator.helpers import FormHelper
from django_clite.commands.generator.helpers import ModelHelper
from django_clite.commands.generator.helpers import SerializerHelper
from django_clite.commands.generator.helpers import TestHelper
from django_clite.commands.generator.helpers import ViewSetHelper


BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]

CURRENT_WORKING_DIRECTORY = '.'

PREVIOUS_WORKING_DIRECTORY = '..'

DEFAULT_APP_PACKAGES = {
    'admin', 'fixtures', 'forms',
    'middleware', 'models', 'serializers',
    'templates', 'views', 'viewsets'
}

REUSABLE_APP = {
    'README.rst': 'README_rst.tpl',
    'MANIFEST.in': 'MANIFEST.tpl',
    'LICENSE': 'LICENSE.tpl',
    'setup.cfg': 'setup_cfg.tpl',
    'setup.py': 'setup.tpl',
}

SETTINGS = {
    'settings.py': 'settings.tpl'
}

# CLI_TEMPLATES = {
#     '.config.json': 'cli-config_json.tpl'
# }

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

UNWANTED_FILES = {
    'apps.py', 'admin.py', 'models.py',
    'tests.py', 'views.py', '__init__.py'
}

APP_TEMPLATES = {
    'api.py': 'api.tpl',
    'urls.py': 'urls.tpl',
    'apps.py': 'apps.tpl'
}


class CustomAppType(Enum):

    def _generate_next_value_(self, start, count, last_values):
        return inflection.underscore(self)

    Authentication = 'auto()'
    ActiveRecord = auto()


class CreatorHelper(FSHelper):
    """
    Creator Helper

    Aids the creation of projects and apps.
    Class has access to file system through FSHelper.
    """

    def __init__(self, cwd, dry=False, force=False, default=False, verbose=False):
        super(CreatorHelper, self).__init__(cwd, dry, force, default, verbose)

    def __celery(self, project):
        # Add celery to proj/proj/__init__.py
        os.chdir(project)
        os.chdir(project)
        self.parse_templates(
            parings={'__init__.py': 'celery_init.tpl'},
            names=TEMPLATES,
            directory=TEMPLATE_DIR,
            force=True,
            context={'project': project}
        )
        os.chdir(PREVIOUS_WORKING_DIRECTORY)
        os.chdir(PREVIOUS_WORKING_DIRECTORY)

    def __git(self, project, origin):
        os.chdir(project)

        if not self.is_dry:
            self.create_repository()
            subprocess.check_output(['git', 'remote', 'add', 'origin', origin])
            log_success(f'Successfully added origin {origin}')
            return True
        log_success("Skipping adding remote origin")
        return False

        # Return to top of project directory
        os.chdir(PREVIOUS_WORKING_DIRECTORY)

    def __project(self, project, presets=[], **kwargs):
        """
        Creates a django project with or without customizations

        :param project: django project name
        :param presets: default options for django project
        :return: None
        """

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

        # Generating project directory with the help of `django-admin`
        if not self.is_dry:
            try:
                log_verbose(header=f'Attempting to create project: {project}')
                subprocess.check_output([
                    'django-admin',
                    'startproject',
                    project
                ])
            except subprocess.CalledProcessError:
                log_error(DEFAULT_ERRORS['project'])
                raise click.Abort

            if presets:
                # Customize django project directory
                os.chdir(project)

                for preset in presets:
                    depth = 0

                    if preset == 'celery':
                        os.chdir(project)
                        self.create_package(project=project, package='celery')
                        os.chdir('celery')
                        depth += 2

                    if preset in ['custom_settings', 'custom_storage']:
                        os.chdir(project)
                        depth += 1

                    # Parse templates
                    self.parse_templates(
                        parings=supported_presets[preset],
                        names=TEMPLATES,
                        directory=TEMPLATE_DIR,
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
                        os.chdir(PREVIOUS_WORKING_DIRECTORY)

                # Return to top of project directory
                os.chdir(PREVIOUS_WORKING_DIRECTORY)

    def __custom_app(self, project, app, base, **kwargs):

        paths = {
            'admin': f'{base}/admin',
            'forms': f'{base}/forms',
            'models': f'{base}/models',
            'serializers': f'{base}/serializers',
            'models_test': f'{base}/models/tests',
            'serializers_test': f'{base}/serializers/tests',
            'viewsets': f'{base}/viewsets'
        }

        t = kwargs.get('type')

        if t == CustomAppType.Authentication:
            AdminHelper(cwd=paths['admin']).create_auth_user()
            FormHelper(cwd=paths['forms']).create_auth_user()
            ModelHelper(cwd=paths['models']).create_auth_user()
            SerializerHelper(cwd=paths['serializers']).create_auth_user()
            ViewSetHelper(cwd=paths['viewsets']).create(model='user')
            TestHelper(cwd=paths['models_test']).create_auth_user(scope='model')
            TestHelper(cwd=paths['serializers_test']).create_auth_user(scope='serializer')

            # return to application directory
            os.chdir(base)

        if t == CustomAppType.ActiveRecord:
            self.create_app(project=project, app=app, active_record=True)

    def create_app_package(self, package, project, app):
        """
        Create an app package and any associated sub-packages or modules
        """

        package = sanitized_string(package)
        app = sanitized_string(app)

        # Create app package
        self.create_package(
            project=project,
            package=package,
            app=app
        )

        # Package customizations
        os.chdir(package)

        if self.verbose:
            log_verbose(header=f'Customizations for "{package}":', message='')

        self.create_package(project=project, package='helpers', app=app)
        if package == 'admin':
            self.create_package(project=project, package='actions', app=app)
            self.create_package(project=project, package='inlines', app=app)
            self.create_package(project=project, package='permissions', app=app)
        if package == 'audit':
            filename = '__init__.py'
            index = TEMPLATES.index('audit.tpl')
            template = TEMPLATES[index]

            content = rendered_file_template(
                path=TEMPLATE_DIR,
                template=template,
                context={'project': project, 'app': app}
            )

            self.create_file(
                path=os.getcwd(),
                filename=filename,
                content=content,
                force=True,
            )
        if package == 'models':
            self.create_package(project=project, package='managers', app=app)
            self.create_package(project=project, package='signals', app=app)
            self.create_package(project=project, package='tests', app=app)
            self.create_package(project=project, package='validators', app=app)
            self.create_package(project=project, package='permissions', app=app)
        if package == 'serializers':
            self.create_package(project=project, package='tests', app=app)
        if package == 'templates':
            self.create_package(project=project, package='tags', app=app)
        if package == 'views':
            filename = 'routes.py'
            index = TEMPLATES.index('routes.tpl')
            template = TEMPLATES[index]

            content = rendered_file_template(
                path=TEMPLATE_DIR,
                template=template,
                context={'project': project, 'app': app}
            )

            self.create_file(
                path=os.getcwd(),
                filename=filename,
                content=content,
            )
        if package == 'viewsets':
            self.create_package(project=project, package='permissions', app=app)
            filename = 'router.py'
            index = TEMPLATES.index('router.tpl')
            template = TEMPLATES[index]

            content = rendered_file_template(
                path=TEMPLATE_DIR,
                template=template,
                context={'project': project, 'app': app}
            )

            self.create_file(
                path=os.getcwd(),
                filename=filename,
                content=content,
            )

        os.chdir(PREVIOUS_WORKING_DIRECTORY)

        if self.verbose:
            log_verbose(header=f'Finished customizing "{package}" package.', message='')

    def create_app(self, project, app, auth=False, **kwargs):
        """
        :param project: name of django project
        :param app: name of django app
        :param auth: app is used for authentication
        :param kwargs:
        :return: True if app is created. False otherwise
        """

        project = sanitized_string(project)
        app = sanitized_string(app)

        if self.verbose:
            log_verbose(header=f'Creating app {app}:', message=f'\tLocation: {os.getcwd()}')

        # Create django application
        try:
            subprocess.check_output([
                'django-admin',
                'startapp',
                app
            ])
        except subprocess.CalledProcessError:
            log_error(DEFAULT_ERRORS['app'].format(app))
            return False

        # Perform app customizations
        os.chdir(app)

        if self.verbose:
            log_verbose(header='Customizations:', message=f'\t{app}')

        # Remove unwanted files
        try:
            for unwanted in UNWANTED_FILES:
                os.remove(unwanted)
        except FileNotFoundError:
            pass

        if self.verbose:
            log_verbose(header="Removed unwanted modules:", message=f'\t{UNWANTED_FILES}')

        # Parse templates for apps.py and urls.py
        try:
            for filename, template in APP_TEMPLATES.items():
                content = rendered_file_template(
                    path=TEMPLATE_DIR,
                    template=template,
                    context={'project': project, 'app': app}
                )

                self.create_file(
                    path=os.getcwd(),
                    filename=filename,
                    content=content
                )
        except OSError:
            pass

        # Create app-specific packages and module
        if kwargs.get('api'):
            DEFAULT_APP_PACKAGES.remove('admin')
            DEFAULT_APP_PACKAGES.remove('forms')
            DEFAULT_APP_PACKAGES.remove('templates')
            DEFAULT_APP_PACKAGES.remove('views')

        if kwargs.get('audit_record'):
            DEFAULT_APP_PACKAGES.add('audit')

        for package in DEFAULT_APP_PACKAGES:
            try:
                self.create_app_package(
                    package=package,
                    project=project,
                    app=app
                )
            except OSError as e:
                log_error(f"Cannot create package: {package}\n{e}")

        if auth:
            if self.verbose:
                log_verbose(header=f'Adding custom user model in {app}', message='')

            self.__custom_app(
                project=project,
                app=app,
                base=os.getcwd(),
                type=CustomAppType.Authentication
            )

        os.chdir(PREVIOUS_WORKING_DIRECTORY)
        log_success(DEFAULT_APP_CREATION_LOG.format(app))

        return True

    def create_project(self, presets, project, apps, **kwargs):
        """
        Creates a project structure and its dependent packages
        """

        # Create project
        self.__project(project, presets, **kwargs)

        # Add customizations for celery
        if 'celery' in presets:
            self.__celery(project)
        
        # Add apps to django project
        if apps:
            for app in apps:
                os.chdir(project)
                os.chdir(project)

                self.create_app(project=project, app=app)

                os.chdir(PREVIOUS_WORKING_DIRECTORY)
                os.chdir(PREVIOUS_WORKING_DIRECTORY)

        # Add special apps to django project
        if kwargs.get('default_apps'):
            for app in kwargs.get('default_apps'):
                auth = app == 'authentication'
                active_record = app == 'active_record'

                os.chdir(project)
                os.chdir(project)

                self.create_app(
                    project=project,
                    app=app,
                    auth=auth,
                    active_record=active_record
                )

                os.chdir(PREVIOUS_WORKING_DIRECTORY)
                os.chdir(PREVIOUS_WORKING_DIRECTORY)

        # Create git repository
        if 'git' in presets:
            self.__git(project, origin=kwargs.get('origin'))

        return True
 
    def create_scoped_file(self, project, template, filename, apps=None):
        content = rendered_file_template(
            path=TEMPLATE_DIR,
            template=template,
            context={'project': project, 'apps': apps}
        )

        return self.create_file(
            content=content,
            filename=filename,
        )
