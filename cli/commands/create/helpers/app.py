import os
import subprocess
import inflection
from datetime import datetime
from enum import Enum, auto
from cli.helpers.logger import *
from cli.helpers import FSHelper
from cli.helpers import sanitized_string
from cli.helpers import rendered_file_template
from cli.helpers.errors import DEFAULT_ERRORS
from cli.commands.generate.helpers import AdminHelper
from cli.commands.generate.helpers import FormHelper
from cli.commands.generate.helpers import ModelHelper
from cli.commands.generate.helpers import SerializerHelper
from cli.commands.generate.helpers import TestHelper
from cli.commands.generate.helpers import ViewSetHelper
from cli.decorators import watch_templates

now = datetime.now

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

CURRENT_WORKING_DIRECTORY = '.'

PREVIOUS_WORKING_DIRECTORY = '..'

DEFAULT_APP_PACKAGES = {
    'admin',
    'fixtures',
    'forms',
    'middleware',
    'models',
    'serializers',
    'templates',
    'views',
    'viewsets',
}

UNWANTED_FILES = {
    'apps.py',
    'admin.py',
    'models.py',
    'tests.py',
    'views.py',
    '__init__.py'
}

APP_TEMPLATES = {
    'api.py': 'api.tpl',
    'urls.py': 'urls.tpl',
    'apps.py': 'apps.tpl',
    'requires.py': 'requires.tpl',
    '__init__.py': 'init.tpl',
}

APP_PACKAGE_FILES = {
    '.gitignore': 'gitignore.tpl',
    'LICENSE.md': 'LICENSE.tpl',
    'MANIFEST.in': 'MANIFEST.tpl',
    'README.md': 'README.tpl',
    'setup.cfg': 'setup_cfg.tpl',
    'setup.py': 'setup.tpl',
}


class CustomAppType(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return inflection.underscore(self)

    Authentication = 'auto()'
    ActiveRecord = auto()


@watch_templates(os.path.join(BASE_DIR, 'templates/app'))
class AppHelper(FSHelper):
    """
    Creator Helper

    Aids the creation of projects and apps.
    Class has access to file system through FSHelper.
    """

    def __init__(self, cwd, package=False, dry=False, force=False, default=False, verbose=False):
        self.package = package
        super(AppHelper, self).__init__(cwd, dry, force, default, verbose)

    def __custom_app(self, project, app, base, **kwargs):
        """
        :param project: name of django project
        :param app: name of app
        :param base: path to app directory
        :param kwargs:
        :return: None
        """
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
            self.change_directory(base)

        if t == CustomAppType.ActiveRecord:
            self.create_app(project=project, app=app, active_record=True)

    def create_app_package(self, package, project, app):
        """
        Create an app package and any associated sub-packages or modules

        :param package: name of app package
        :param project: name of django project
        :param app: name of app
        :return: None
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
        self.change_directory(package)

        if self.verbose:
            log_verbose(header=f'Customizations for "{package}":', message='')

        self.create_package(project=project, package='helpers', app=app)
        if package == 'admin':
            self.create_package(project=project, package='actions', app=app)
            self.create_package(project=project, package='inlines', app=app)
            self.create_package(project=project, package='permissions', app=app)
        if package == 'audit':
            filename = '__init__.py'
            index = self.TEMPLATE_FILES.index('audit.tpl')
            template = self.TEMPLATES_DIRECTORY[index]

            content = rendered_file_template(
                path=self.TEMPLATES_DIRECTORY,
                template=template,
                context={
                    'app': app,
                    'classname': inflection.camelize(app),
                    'package': package,
                    'project': project,
                }
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
            index = self.TEMPLATE_FILES.index('routes.tpl')
            template = self.TEMPLATE_FILES[index]

            content = rendered_file_template(
                path=self.TEMPLATES_DIRECTORY,
                template=template,
                context={
                    'app': app,
                    'classname': inflection.camelize(app),
                    'package': self.package,
                    'project': project,
                }
            )

            self.create_file(
                path=os.getcwd(),
                filename=filename,
                content=content,
            )
        if package == 'viewsets':
            self.create_package(project=project, package='permissions', app=app)
            filename = 'router.py'
            index = self.TEMPLATE_FILES.index('router.tpl')
            template = self.TEMPLATE_FILES[index]

            content = rendered_file_template(
                path=self.TEMPLATES_DIRECTORY,
                template=template,
                context={
                    'app': app,
                    'package': self.package,
                    'project': project,
                }
            )

            self.create_file(
                path=os.getcwd(),
                filename=filename,
                content=content,
            )

        self.change_directory(PREVIOUS_WORKING_DIRECTORY)

        if self.verbose:
            log_verbose(header=f'Finished customizing "{package}" package.', message='')

    def create_app(self, app, auth=False, project=None, **kwargs):
        """
        Creates a django app and customizes its directory

        :param project: name of django project
        :param app: name of django app
        :param auth: app is used for authentication
        :param kwargs:
        :return: app directory. None if an error occurred.
        """

        project = '' if not project else sanitized_string(project)
        app = sanitized_string(app)

        if self.is_dry:
            if self.verbose:
                log_standard(f'Skipping creation of app {app} with --dry enabled')
            return False

        if self.verbose:
            log_verbose(header=f'Creating app {app}:', message=f'\tLocation: {os.getcwd()}')

        # Create django application
        try:
            if self.package:
                self.make_directory(app)
                self.change_directory(app)

            subprocess.check_output([
                'django-admin',
                'startapp',
                app
            ])
        except subprocess.CalledProcessError:
            log_error(DEFAULT_ERRORS['app'].format(app))
            return False

        # Add license, setup.py, and other files
        if self.package:
            try:
                for filename, template in APP_PACKAGE_FILES.items():
                    content = rendered_file_template(
                        path=self.TEMPLATES_DIRECTORY,
                        template=template,
                        context={
                            'app': app,
                            'app_namespace': app,
                            'classname': inflection.camelize(app),
                            'package': self.package,
                            'project': project,
                            'year': datetime.today().year,
                            **kwargs,
                        }
                    )

                    self.create_file(
                        path=os.getcwd(),
                        filename=filename,
                        content=content
                    )
            except OSError:
                pass

        # Perform app customizations
        self.change_directory(app)
        directory = os.getcwd()
        FSHelper.config['apps'].append({
            'app': app,
            'path': directory,
            'created_at': now().strftime("%d/%m/%Y %H:%M:%S"),
            'updated_at': now().strftime("%d/%m/%Y %H:%M:%S"),
        })

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
                    path=self.TEMPLATES_DIRECTORY,
                    template=template,
                    context={
                        'app': app,
                        'classname': inflection.camelize(app),
                        'package': self.package,
                        'project': project,
                    }
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

        self.change_directory(PREVIOUS_WORKING_DIRECTORY)
        log_success(DEFAULT_APP_CREATION_LOG.format(app))

        return directory
