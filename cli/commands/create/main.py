import click
import os
import inquirer
from datetime import datetime
from cli.helpers import get_project_name
from cli.helpers import find_project_files
from cli.helpers.logger import *
from cli.commands.inspect.main import InspectorHelper
from cli.commands.inspect.main import inspect
from cli.commands.create.helpers.app import AppHelper
from cli.commands.create.helpers.creator import CreatorHelper
from cli.commands.create.presets import extra_apps
from cli.commands.create.presets import installable_apps
from cli.commands.create.presets import presets
# from cli.commands.generate.main import not_an_app_directory_warning


def wrong_place_warning(ctx):
    if (ctx.obj['path'] and ctx.obj['project_name']) is None:
        log_error(DEFAULT_MANAGEMENT_ERROR)
        log_standard('')
        log_standard(DEFAULT_MANAGEMENT_ERROR_HELP)
        raise click.Abort


def inquire_project_presets(project_name, default=False):

    remotes = {
        'github': 'git@github.com',
        'gitlab': 'git@gitlab.com',
        'bitbucket': 'git@bitbucket.org',
    }

    # ------------------------------------------
    # Default installation
    if default:
        return {
            'presets': presets.DEFAULTS,
            'custom_apps': [extra_apps.DEFAULTS],
            'remote': remotes['github'],
            'author': os.environ.get('USER'),
            'user': os.environ.get('USER'),
            'repository': project_name,
            'origin': f"{remotes['github']}:{os.environ.get('USER')}/{project_name}.git",
            'year': datetime.year,
        }
    # ------------------------------------------

    # ------------------------------------------
    # Customized installation
    # ------------------------------------------
    project_questions = [
        inquirer.Checkbox(
            'presets', message='supported presets', choices=sorted(presets.PRESETS), default=presets.DEFAULTS
        ),
        inquirer.Checkbox(
            'custom_apps', message='custom apps', choices=extra_apps.EXTRA_APPS, default=extra_apps.DEFAULTS
        ),
        inquirer.List('remote', message='remote', choices=[r for r in remotes], carousel=True),
        inquirer.Text('author', message='package author', default=os.environ.get('USER')),
        inquirer.Text('user', message='repository user/organization', default=os.environ.get('USER')),
        inquirer.Text('repository', message='repository name', default=project_name),
    ]

    # Get answers
    answers = inquirer.prompt(project_questions)

    # Remote origin URL
    answers['origin'] = f"{remotes[answers['remote']]}:{answers['user']}/{answers['repository']}.git"

    answers['year'] = datetime.year

    return answers


def inquire_installable_apps(default=False):
    apps = []
    middleware = []

    if default:
        apps = [a for a in installable_apps.DEFAULTS]
        middleware = [
            app for a in installable_apps.INSTALLABLE_APPS
            if a in installable_apps.DEFAULTS
            for app in installable_apps.INSTALLABLE_APPS[a]['middleware']
        ]
        return apps, middleware

    if click.confirm('Would you like to add apps to your INSTALLED_APPS?'):
        installed_apps_questions = [
            inquirer.Checkbox(
                'install', message='install default apps', choices=sorted(installable_apps.INSTALLABLE_APPS),
                default=installable_apps.DEFAULTS
            ),
        ]

        # Determine installed apps
        app_answers = inquirer.prompt(installed_apps_questions)['install']
        apps = [
            app for a in installable_apps.INSTALLABLE_APPS
            if a in app_answers
            for app in installable_apps.INSTALLABLE_APPS[a]['apps']
        ]

        middleware = [
            app for a in installable_apps.INSTALLABLE_APPS
            if a in app_answers
            for app in installable_apps.INSTALLABLE_APPS[a]['middleware']
        ]

    return apps, middleware


def inquire_docker_options(default=False):
    # Install
    # - celery
    # - vault
    # - consul
    # - redis
    values = []
    return values


def inquire_app_presets(app, default=False):

    remotes = {
        'github': 'git@github.com',
        'gitlab': 'git@gitlab.com',
        'bitbucket': 'git@bitbucket.org',
    }

    # ------------------------------------------
    # Default installation
    if default:
        return {
            'remote': remotes['github'],
            'author': os.environ.get('USER'),
            'user': os.environ.get('USER'),
            'repository': app,
            'origin': f"{remotes['github']}:{os.environ.get('USER')}/{app}.git",
            'url': f"https://{remotes['github']}.com/{os.environ.get('USER')}/{app}",
            'year': datetime.year,
        }
    # ------------------------------------------

    # ------------------------------------------
    # Customized installation
    # ------------------------------------------
    project_questions = [
        inquirer.List('remote', message='remote', choices=[r for r in remotes], carousel=True),
        inquirer.Text('author', message='package author', default=os.environ.get('USER')),
        inquirer.Text('user', message='repository user/organization', default=os.environ.get('USER')),
        inquirer.Text('repository', message='repository name', default=app),
        inquirer.Text('url', mesage='', default=f"https://{remotes['github']}.com/{os.environ.get('USER')}/{app}"),
    ]

    # Get answers
    answers = inquirer.prompt(project_questions)

    # Remote origin URL
    answers['origin'] = f"{remotes[answers['remote']]}:{answers['user']}/{answers['repository']}.git"

    answers['year'] = datetime.year

    return answers


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
@click.option('--defaults', is_flag=True, help="Apply defaults to project")
@click.pass_context
def project(ctx, name, apps, defaults):
    """
    Creates a new django project.

    This is similar to using `django-admin startproject project_name` but with some added functionality.
    The command can handle the creation of apps upon creation of any project, you can simply specify the name of
    the apps after the project name:

        D new project website app1 app2 app3 ...
    """

    helper = ctx.obj['helper']

    # project presets
    project_presets = inquire_project_presets(project_name=name, default=defaults)

    # project app settings
    project_apps, project_middleware = inquire_installable_apps(default=defaults)

    # docker settings
    # x_docker = inquire_docker_options()

    # Create project
    return helper.create_project(
        project=name,
        apps=apps,
        settings_apps=project_apps,
        settings_middleware=project_middleware,
        **project_presets,
    )


@create.command(name='apps')
@click.argument('apps', nargs=-1)
@click.option('--project-name', '-p', help="Specify name of your project.")
@click.option('--package', is_flag=True, help="Specify that the app can be installed as a package.")
@click.option('--directory', '-d', type=click.Path(), help="Specify path to your project's management file.")
@click.option('--api', is_flag=True, help="Add a special api urls module to your app directory.")
@click.option('--defaults', is_flag=True, help="Apply defaults to project")
@click.pass_context
def applications(ctx, apps, project_name, package, directory, api, defaults):
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

    if package:
        path = os.getcwd()
        __project_name = 'django-package'
    elif not os.path.exists(path):
        log_error(DEFAULT_MANAGEMENT_ERROR)
        log_standard('')
        log_standard(DEFAULT_MANAGEMENT_ERROR_HELP)
        raise click.Abort()

    helper = AppHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        verbose=ctx.obj['verbose'],
        package=package,
    )

    auth_application = None

    for name in apps:
        options = inquire_app_presets(name, default=defaults)
        helper.create_app(
            project=__project_name,
            app=name,
            api=api,
            **options,
        )

        click.echo(f"Successfully created app: {name}")


@create.command()
@click.option('--ignore-apps', is_flag=True, help="Do not add project apps to INSTALLED_APPS.")
@click.option('--override-file', is_flag=True, help="Override contents of current settings.py module")
@click.pass_context
def settings(ctx, ignore_apps, override_file):
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
        h.create_file_in_context(
            project=ctx.obj['project_name'],
            template='settings.tpl',
            filename='settings_override.py',
            apps=apps
        )
    else:
        h.create_file_in_context(
            project=ctx.obj['project_name'],
            template='settings.tpl',
            filename='settings_override.py',
        )
