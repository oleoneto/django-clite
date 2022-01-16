import os
import click
import subprocess
from pathlib import PosixPath
from rich.live import Live
from rich.prompt import Confirm
from rich import print as rich_print
from cli.utils.logger import Logger
from cli.utils.sanitize import sanitized_string
from cli.utils.fs.utils import change_directory, inside_project_directory
from cli.handlers.filesystem import FileHandler, GitHandler, TemplateHandler
from cli.handlers.filesystem.directory import Directory
from cli.handlers.filesystem.template import Template


initializer_template = Template('__init__.py', '# import package modules here', raw=True)


def format_application(ctx, param, value):
    apps = []
    files = [
        initializer_template,
        Template('apps.py', 'apps.tpl'),
        Template('urls.py', 'urls.tpl'),
        Template('constants.py', '# your constants go here', raw=True),
    ]
    children = [
        Directory(
            'admin',
            [
                Directory('actions', files=[initializer_template]),
                Directory('inlines', files=[initializer_template]),
                Directory('permissions', files=[initializer_template])
            ],
            [initializer_template]
        ),
        Directory('fixtures', files=[initializer_template]),
        Directory('forms', files=[initializer_template]),
        Directory('middleware', files=[initializer_template]),
        Directory('migrations', files=[initializer_template]),
        Directory(
            'models',
            [
                Directory('managers', [], [initializer_template]),
                Directory('signals', [], [initializer_template]),
                Directory('validators', [], [initializer_template])
            ],
            [initializer_template]
        ),
        Directory(
            'router',
            files=[
                Template('__init__.py', 'from .api import urlpatterns\nfrom .router import router', raw=True),
                Template('api.py', 'api.tpl'),
                Template('router.py', 'router.tpl')
            ]
        ),
        Directory('serializers', files=[initializer_template]),
        Directory('tasks', files=[initializer_template]),
        Directory('templates', files=[]),
        Directory('templatetags', files=[initializer_template]),
        Directory(
            'tests',
            files=[Template('__init__.py', 'from .models import *\nfrom .viewsets import *', raw=True)],
            children=[
                Directory('models', files=[initializer_template]),
                Directory('viewsets', files=[initializer_template])
            ]
        ),
        Directory('views', files=[initializer_template]),
        Directory(
            'viewsets',
            [Directory('permissions'), Directory('mixins')],
            [initializer_template]
        ),
    ]

    is_package = ctx.params.get('is_package')

    for app_name in value:
        if is_package:
            files.extend([
                Template('LICENSE', 'LICENSE.tpl'),
                Template('MANIFEST', 'MANIFEST.tpl'),
                Template('README.md', 'README.tpl'),
                Template('setup.cfg', 'setup_cfg.tpl'),
                Template('setup.py', 'setup.tpl'),
            ])
            children = [
                Directory(
                    sanitized_string(app_name),
                    children,
                    files=[Template('__init__.py', 'init.tpl')]
                )
            ]

        application = Directory(
            name=sanitized_string(app_name),
            verbose=ctx.obj['verbose'],
            force=ctx.obj['force'],
            dry=ctx.obj['dry'],
            children=children,
            files=files,
            templates_scope='app',
        )

        apps.append(application)

    return apps


@click.group()
@click.pass_context
def new(ctx):
    """
    Creates projects and apps.
    """
    ctx.ensure_object(dict)


@new.command(name='project')
@click.argument('name')
@click.argument('apps', nargs=-1, callback=format_application)
@click.option('--defaults', is_flag=True, help="Apply defaults to project")
@click.pass_context
def create_project(ctx, name, apps, defaults):
    """
    Creates a new django project.

    This is similar to using `django-admin startproject project_name` but with some added functionality.
    The command can handle the creation of apps upon creation of any project, you can simply specify the name of
    the apps after the project name:

        django-clite new project website app1 app2 app3 ...
    """

    # FIXME: Handle --defaults flag
    # FIXME: Consolidate both settings.py modules

    project = Directory(
        sanitized_string(name),
        children=[
            Directory('config', files=[
                Template('database.py', '# database', raw=True),
                Template('storage.py', 'storage.tpl'),
                Template('settings.py', 'settings.tpl'),
            ]),
            Directory('celery', files=[
                Template('__init__.py', 'celery.tpl'),
                Template('tasks.py', 'celery_tasks.tpl'),
            ]),
        ],
        files=[
            Template('__init__.py', '# import package modules here', raw=True),
            Template('.env', 'env.tpl'),
            Template('.env-example', 'env.tpl'),
            Template('.gitignore', 'gitignore.tpl'),
            Template('Dockerfile', 'dockerfile.tpl'),
            Template('docker-compose.yml', 'docker-compose.tpl'),
            Template('docker-entrypoint.sh', 'docker-entrypoint.tpl'),
            Template('README.md', 'README.tpl'),
            Template('Procfile', 'procfile.tpl'),
            Template('urls.py', 'urls.tpl'),
        ],
        templates_scope="project",
    )

    scoped_context = {
        'verbose': ctx.obj['verbose'],
        'force': ctx.obj['force'],
        'dry': ctx.obj['dry'],
    }

    template_handler = TemplateHandler(scope='project', **scoped_context)

    try:
        with Live(f'Creating django project [b][yellow]{project.name}') as live:
            try:
                if not ctx.obj['dry']:
                    subprocess.check_output(['django-admin', 'startproject', project.name])
            except subprocess.CalledProcessError as error:
                return Logger.error(error.__str__())

            # Configuration should be under > project
            change_directory(project.name, **scoped_context)

            project.create(template_handler, create_in_cwd=True, **scoped_context)

        if apps:
            change_directory(project.name, **scoped_context)

            ctx.invoke(create_applications, apps=apps, directory=os.getcwd())

            change_directory('..')

        # Initialize git repository
        GitHandler.initialize(**scoped_context)

        Logger.log(f'Successfully created django project [b][yellow]{project.name}')
    except (KeyboardInterrupt, SystemExit, Exception) as error:
        Logger.error(f'An exception occurred while creating this project: [b]{repr(error.__str__())}\n')


@new.command(name='apps')
@click.argument('apps', nargs=-1, callback=format_application)
@click.option('--directory', '-d', type=click.Path(), help="Specify path to your project's management file.")
@click.pass_context
def create_applications(ctx, apps, directory):
    """
    Creates new django apps.

    This is similar to using `django-admin startapp app_name`
    but adds more structure to your app by creating packages for forms, models,
    serializers, tests, templates, views, and viewsets.

    The command can accept multiple apps as arguments. So,

        django-clite new apps shop blog forum

    will work prompt the CLI to create all 4 apps two levels within your project's
    directory, i.e. my_site/my_site. The CLI tries to identify where the management module for your
    project is, so it can place your app files in the correct location. This helps with consistency
    as the CLI can infer module/package scopes when performing other automatic configurations.

    As part of the CLI convention, each app is assigned its own `urls.py` file, which can be used to route urls on a
    per-app basis. Another convention the CLI adopts is
    to add a viewsets package to the app's directory by default (for use with DRF). Within the viewsets directory
    a DRF router is instantiated in `router.py` and its urls added to each app's urlpatterns by default.
    """

    if directory:
        ctx.obj['project_files'] = FileHandler.find_files(directory, patterns=['manage.py', 'wsgi.py', 'apps.py'])

    scoped_context = {
        'verbose': ctx.obj['verbose'],
        'force': ctx.obj['force'],
        'dry': ctx.obj['dry'],
    }

    template_handler = TemplateHandler(scope='app', **scoped_context)

    # Attempt to create app inside a project as prompt user for choice if outside project directory
    if inside_project_directory(ctx, exit_on_error=not scoped_context['force']):
        server_file = ctx.obj['project_files'].get('wsgi.py', None) or ctx.obj['project_files'].get('asgi.py', None)
        management_file = ctx.obj['project_files'].get('manage.py', None)

        project_path = PosixPath(directory) if directory else FileHandler.scoped_project_directory(management_file or server_file)

        if not project_path:
            raise click.Abort
    else:
        if not Confirm.ask('The CLI could not find your django project. Proceed anyways?', default=False):
            raise click.Abort

    try:
        # Create application inside the scoped path
        change_directory(project_path)

        for app in apps:
            template_handler.context = {'project': project_path.name, 'app': app.name, **scoped_context}

            app.create(template_handler, **scoped_context)

            if scoped_context['verbose']:
                Logger.log(f"Successfully created created app [b]{app.name}[/b] with the following structure:")
                rich_print(app.traverse(show_files=False))
            else:
                Logger.log(f"Successfully created app [b]{app.name}")
    except (KeyboardInterrupt, SystemExit, Exception) as error:
        Logger.error(repr(error))
