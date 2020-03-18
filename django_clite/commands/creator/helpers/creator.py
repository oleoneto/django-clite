import os
import subprocess
from django_clite.helpers.logger import *
from django_clite.helpers import FSHelper
from django_clite.helpers import sanitized_string
from django_clite.helpers import rendered_file_template
from django_clite.commands.generator.helpers import (
    AdminHelper,
    FormHelper,
    ModelHelper,
    SerializerHelper,
    TestHelper,
    ViewSetHelper
)


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

DOKKU_TEMPLATES = {
    'app.json': 'app_json.tpl',
    'CHECKS': 'dokku_checks.tpl',
    'DOKKU_SCALE': 'dokku_scale.tpl',
    'Procfile': 'procfile.tpl',
}

TOP_LEVEL_TEMPLATES = {
    'CHECKS': 'dokku_checks.tpl',
    'Dockerfile': 'dockerfile.tpl',
    'docker-compose.yml': 'docker-compose.tpl',
    'docker-entrypoint.sh': 'docker-entrypoint.tpl',
    'Pipfile': 'Pipfile.tpl',
    'README.md': 'README.tpl',
    '.env': 'env.tpl',
    '.env-example': 'env.tpl',
    '.gitignore': 'gitignore.tpl',
}

INNER_LEVEL_TEMPLATES = {
    'settings_override.py': 'settings.tpl',
    'storage.py': 'storage.tpl',
}

UNWANTED_FILES = {
    'apps.py', 'admin.py', 'models.py',
    'tests.py', 'views.py', '__init__.py'
}

APP_TEMPLATES = {
    'urls.py': 'urls.tpl',
    'apps.py': 'apps.tpl'
}


class CreatorHelper(FSHelper):
    """
    Creator Helper

    Aids the creation of projects and apps.
    Class has access to file system through FSHelper.
    """

    def __init__(self, cwd, dry=False, force=False, default=False, verbose=False):
        super(CreatorHelper, self).__init__(cwd, dry, force, default, verbose)

    def create_project(self, project, apps, **kwargs):
        """
        Creates a project structure and its dependent packages
        """

        project = sanitized_string(project)

        # Generating project directory
        # with the help of `django-admin`
        if not self.is_dry:
            try:
                log_standard(f"Attempting to create project: {project}")
                subprocess.check_output([
                    'django-admin',
                    'startproject',
                    project
                ])
            except subprocess.CalledProcessError:
                log_error(DEFAULT_ERRORS['project'])
                raise click.Abort

        # Customize django project directory
        os.chdir(project)

        # Create top-level directories and top-level files
        folders = ['dokku', 'dummy']

        if kwargs.get('default') or kwargs.get('dokku'):
            self.parse_templates(
                parings=TOP_LEVEL_TEMPLATES,
                names=TEMPLATES,
                directory=TEMPLATE_DIR,
                folders=folders,
                context={
                    'project': project,
                    'timeout': 60,
                    'wait': 20,
                    'web': 1,
                }
            )

            # Customize Dokku configuration
            os.chdir('dokku')
            self.parse_templates(
                parings=DOKKU_TEMPLATES,
                names=TEMPLATES,
                directory=TEMPLATE_DIR,
                context={
                    'project': project,
                    'timeout': 60,
                    'wait': 20,
                    'web': 1,
                }
            )
            os.chdir(PREVIOUS_WORKING_DIRECTORY)

        # Customize project package
        os.chdir(project)
        self.parse_templates(
            parings=INNER_LEVEL_TEMPLATES,
            names=TEMPLATES,
            directory=TEMPLATE_DIR,
            context={
                'project': project,
                'apps': apps,
            }
        )

        # Create project apps inside the inner package
        if apps is not None:
            for app in apps:
                self.create_app(project=project, app=app)

        # Create optional `custom-auth`
        auth_app = 'authentication'
        if kwargs.get('custom_auth'):
            if self.create_app(
                project=project,
                app=auth_app,
                auth=True
            ):

                auth_app_path = os.getcwd()
                log_error(auth_app_path)

                log_error("Cannot create authentication app.")
                log_error(os.getcwd())

                # Handle authentication app
                os.chdir(auth_app)
                self.__handle_custom_auth(project=project, **kwargs)
                os.chdir(PREVIOUS_WORKING_DIRECTORY)

        # cd ../../
        os.chdir(PREVIOUS_WORKING_DIRECTORY)
        os.chdir(PREVIOUS_WORKING_DIRECTORY)

        # Create git repository
        self.create_repository()

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
            log_info(f"Performing customizations for {package}")

        self.create_package(project=project, package='helpers', app=app)
        if package == 'admin':
            self.create_package(project=project, package='actions', app=app)
            self.create_package(project=project, package='inlines', app=app)
            self.create_package(project=project, package='permissions', app=app)
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
            log_info(f"Finished customizing {package}")

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
            log_info(f"Creating {app} at {os.getcwd()}")

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
            log_info(f"Performing customizations for {app}")

        # Remove unwanted files
        try:
            for unwanted in UNWANTED_FILES:
                os.remove(unwanted)
        except FileNotFoundError:
            pass

        if self.verbose:
            log_standard(f"Removed unwanted modules {UNWANTED_FILES}")

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
                log_info(f"Adding default User model for {app} app")

            self.__handle_custom_auth(project=project, app=app)

        os.chdir(PREVIOUS_WORKING_DIRECTORY)
        log_success(DEFAULT_APP_CREATION_LOG.format(app))

        return True

    def __handle_custom_auth(self, **kwargs):

        project = kwargs.get('project')
        app = kwargs.get('app')

        base = os.getcwd()

        paths = {
            'admin': f'{base}/admin',
            'forms': f'{base}/forms',
            'models': f'{base}/models',
            'serializers': f'{base}/serializers',
            'models_test': f'{base}/models/tests',
            'serializers_test': f'{base}/serializers/tests',
            'viewsets': f'{base}/viewsets'
        }

        AdminHelper(cwd=paths['admin']).create_auth_user()
        FormHelper(cwd=paths['forms']).create_auth_user()
        ModelHelper(cwd=paths['models']).create_auth_user()
        SerializerHelper(cwd=paths['serializers']).create_auth_user()
        ViewSetHelper(cwd=paths['viewsets']).create(model='user')

        TestHelper(cwd=paths['models_test']).create_auth_user(scope='model')
        TestHelper(cwd=paths['serializers_test']).create_auth_user(scope='serializer')

        # return to application directory
        os.chdir(base)

    def create_settings(self, project, apps=None):
        template = 'settings.tpl'
        filename = 'settings_override.py'

        content = rendered_file_template(
            path=TEMPLATE_DIR,
            template=template,
            context={'project': project, 'apps': apps}
        )

        return self.create_file(
            content=content,
            filename=filename,
        )
