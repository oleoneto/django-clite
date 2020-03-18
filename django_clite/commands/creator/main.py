import os
import inquirer
from django_clite.helpers import get_project_name
from django_clite.helpers import find_project_files
from django_clite.helpers.logger import *
from .helpers import *
from django_clite.commands.inspector.main import InspectorHelper
from django_clite.commands.inspector.main import apps as inspect_apps


def wrong_place_warning(ctx):
    if (ctx.obj['path'] and ctx.obj['project_name']) is None:
        log_error(DEFAULT_MANAGEMENT_ERROR)
        log_standard('')
        log_standard(DEFAULT_MANAGEMENT_ERROR_HELP)
        raise click.Abort


@click.group()
@click.pass_context
@click.option('--dry', is_flag=True, help="Display output without creating files.")
@click.option('--default', is_flag=True, help="Apply all default configurations.")
@click.option('--verbose', is_flag=True, help="Run in verbose mode.")
def create(ctx, dry, default, verbose):
    """
    Creates projects and apps.
    """
    ctx.ensure_object(dict)

    ctx.obj['dry'] = dry
    ctx.obj['default'] = default
    ctx.obj['verbose'] = verbose

    ctx.obj['helper'] = CreatorHelper(
        cwd=os.getcwd(),
        dry=dry,
        default=default,
        verbose=verbose
    )

    p, m, f = find_project_files(os.getcwd())  # project path, project directory, management_file

    ctx.obj['path'] = p
    ctx.obj['file'] = f
    ctx.obj['management'] = m
    ctx.obj['project_name'] = get_project_name(f)


@create.command()
@click.argument('name')
@click.option('--docker', is_flag=True, help="Add support for Docker.")
@click.option('--dokku', is_flag=True, help="Add support for Dokku.")
@click.option('-a', '--custom-auth', is_flag=True, help="Add support for custom AUTH_USER_MODEL.")
@click.argument('apps', nargs=-1)
@click.pass_context
def project(ctx, name, docker, dokku, custom_auth, apps):
    """
    Creates a new django project.

    This is similar to using `django-admin startproject project_name` but with some added functionality.
    The command can handle the creation of apps upon creation of any project, you can simply specify the name of
    the apps after the project name:

        D new project website app1 app2 app3 ...

    Another added functionality is the ability to setup Docker and Dokku.
    To do so, use the respective flags --docker and --dokku.

    Also helpful is the ability to initialize your application with a custom authentication model of your choosing.
    When the --custom-auth flag is specified, CLI will add an `authentication` app to your project
    along with a subclass of the AbstractUser model which you can extend for your own authentication purposes.
    """

    helper = ctx.obj['helper']

    helper.create_project(
        project=name,
        apps=apps,
        default=ctx.obj['default'],
        docker=docker,
        dokku=dokku,
        custom_auth=custom_auth,
    )


@create.command()
@click.argument('apps', nargs=-1)
@click.option('--is-auth', is_flag=True, help="Add User for custom authentication.")
@click.option('--project-name', '-p', help="Specify name of your project.")
@click.option('--directory', '-d', type=click.Path(), help="Specify path to your management.")
@click.option('--api', is_flag=True, help="Add a special api urls module to your app directory.")
@click.pass_context
def app(ctx, apps, is_auth, project_name, directory, api):
    """
    Creates new django apps.

    This is similar to using `django-admin startapp app_name`
    but adds more structure to your app by creating packages for forms, models,
    serializers, tests, templates, views, and viewsets.

    The command can accept multiple apps as arguments. So,

        D new app shop blog forum

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

    if is_auth:
        if len(apps) == 1:
            auth_application = apps[0]
        else:
            questions = [
                inquirer.List(
                    'app',
                    message="Which app will be used for authentication?",
                    choices=[name for name in apps],
                ),
            ]
            auth_application = inquirer.prompt(questions)['app']

    for name in apps:
        is_custom_app = (name == auth_application)

        helper.create_app(
            project=__project_name,
            app=name,
            auth=is_custom_app,
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
        default=ctx.obj['default'],
        verbose=ctx.obj['verbose']
    )

    if not ignore_apps:
        ctx.obj['helper'] = InspectorHelper(cwd=ctx.obj['management'])
        apps = ctx.invoke(inspect_apps, no_stdout=True)
        h.create_settings(project=ctx.obj['project_name'], apps=apps)
    else:
        h.create_settings(project=ctx.obj['project_name'])
