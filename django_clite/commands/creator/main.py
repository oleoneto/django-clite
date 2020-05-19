import os
import inquirer
from datetime import datetime
from django_clite.helpers import get_project_name
from django_clite.helpers import find_project_files
from django_clite.helpers.logger import *
from .helpers import *
from django_clite.commands.inspector.main import InspectorHelper
from django_clite.commands.inspector.main import inspect
from django_clite.commands.generator.main import not_an_app_directory_warning


def wrong_place_warning(ctx):
    if (ctx.obj['path'] and ctx.obj['project_name']) is None:
        log_error(DEFAULT_MANAGEMENT_ERROR)
        log_standard('')
        log_standard(DEFAULT_MANAGEMENT_ERROR_HELP)
        raise click.Abort


@click.group()
@click.pass_context
def create(ctx):
    """
    Creates projects and apps.
    """
    ctx.ensure_object(dict)

    ctx.obj['helper'] = CreatorHelper(
        cwd=os.getcwd(),
        dry=ctx.obj['dry'],
        verbose=ctx.obj['verbose']
    )

    p, m, f = find_project_files(os.getcwd())  # project path, project directory, management_file

    ctx.obj['path'] = p
    ctx.obj['file'] = f
    ctx.obj['management'] = m
    ctx.obj['project_name'] = get_project_name(f)


@create.command()
@click.argument('name')
@click.argument('apps', nargs=-1)
@click.pass_context
def project(ctx, name, apps):
    """
    Creates a new django project.

    This is similar to using `django-admin startproject project_name` but with some added functionality.
    The command can handle the creation of apps upon creation of any project, you can simply specify the name of
    the apps after the project name:

        D new project website app1 app2 app3 ...
    """

    helper = ctx.obj['helper']

    year = datetime.year

    presets = ['environments', 'celery', 'dockerized', 'dokku', 'git', 'custom_settings', 'custom_storage']

    default_apps = ['active_record', 'authentication']

    remotes = {
        'github': 'git@github.com',
        'gitlab': 'git@gitlab.com',
        'bitbucket': 'git@bitbucket.org',
    }

    questions = [
        inquirer.Checkbox('presets', message='supported presets', choices=presets, default=[
            p for p in presets if p not in ['custom_settings', 'custom_storage']
            ]
        ),
        inquirer.Checkbox('apps', message='custom apps', choices=default_apps, default=default_apps[1]),
        inquirer.List('remote', message='remote', choices=[r for r in remotes], carousel=True),
        inquirer.Text('author', message='package author', default=os.environ.get('USER')),
        inquirer.Text('user', message='repository user/organization', default=os.environ.get('USER')),
        inquirer.Text('repository', message='repository name', default=name),
    ]

    # Determine presets
    answers = inquirer.prompt(questions)

    # Remote origin URL
    origin = f"{remotes[answers['remote']]}:{answers['user']}/{answers['repository']}.git"

    # Create project
    helper.create_project(
        presets=answers['presets'],
        project=name,
        apps=apps,
        default_apps=answers['apps'],
        author=answers['author'],
        origin=origin,
    )


@create.command(name='apps')
@click.argument('apps', nargs=-1)
@click.option('--project-name', '-p', help="Specify name of your project.")
@click.option('--directory', '-d', type=click.Path(), help="Specify path to your project's management file.")
@click.option('--api', is_flag=True, help="Add a special api urls module to your app directory.")
@click.pass_context
def applications(ctx, apps, project_name, directory, api):
    """
    Creates new django apps.

    This is similar to using `django-admin startapp app_name`
    but adds more structure to your app by creating packages for forms, models,
    serializers, tests, templates, views, and viewsets.

    The command can accept multiple apps as arguments. So,

        D new apps shop blog forum

    will work prompt the CLI to create all 4 apps two levels within your project's
    directory, i.e mysite/mysite. The CLI tries to identify where the management module for your
    project is so it can place your app files in the correct location. This helps with consistency
    as the CLI can infer module/package scopes when performing other automatic configurations.

    As part of the CLI convention, each app is assigned its own `urls.py` file, which can be used to route urls on a per app basis. Another convention the CLI adopts is
    to add a viewsets package to the app's directory by default (for use with DRF). Within the viewsets directory
    a DRF router is instantiated in `router.py` and its urls added to each app's urlpatterns by default.
    """

    # Get project name from arguments
    __project_name = project_name if project_name else ctx.obj['project_name']
    __directory_path = directory if directory else ctx.obj['management']

    try:
        path = os.path.join(__directory_path, __project_name)
    except TypeError:
        path = ''

    if not os.path.exists(path):
        log_error(DEFAULT_MANAGEMENT_ERROR)
        log_standard('')
        log_standard(DEFAULT_MANAGEMENT_ERROR_HELP)
        raise click.Abort()

    helper = CreatorHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        default=ctx.obj['default'],
        verbose=ctx.obj['verbose']
    )

    auth_application = None

    for name in apps:

        helper.create_app(
            project=__project_name,
            app=name,
            api=api,
        )


@create.command()
@click.option('--ignore-apps', is_flag=True, help="Do not add project apps to INSTALLED_APPS.")
@click.pass_context
def settings(ctx, ignore_apps):
    """
    Create settings file for project.
    """

    wrong_place_warning(ctx)
    project_name = ctx.obj['project_name']
    path = os.path.join(ctx.obj['management'], project_name)

    h = CreatorHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        verbose=ctx.obj['verbose']
    )

    if not ignore_apps:
        ctx.obj['helper'] = InspectorHelper(cwd=ctx.obj['management'])
        apps = ctx.invoke(inspect, scope='apps', no_stdout=True)
        h.create_scoped_file(
            project=ctx.obj['project_name'],
            template='settings.tpl',
            filename='settings_override.py',
            apps=apps
        )
    else:
        h.create_scoped_file(
            project=ctx.obj['project_name'],
            template='settings.tpl',
            filename='settings_override.py',
        )
