import os
import click
from django_clite.helpers import get_project_name
from django_clite.helpers import find_project_files
from django_clite.helpers.logger import *
from .helpers import *


def wrong_place_warning(ctx):
    return True if ctx.obj['path'] else False


@click.group()
@click.pass_context
@click.option('--dry', is_flag=True, help="Display output without creating files.")
@click.option('--default', is_flag=True, help="Apply all default configurations.")
def create(ctx, dry, default):
    """
    Creates projects and apps.
    """
    ctx.ensure_object(dict)

    ctx.obj['dry'] = dry
    ctx.obj['default'] = default

    ctx.obj['helper'] = CreatorHelper(
        cwd='.',
        dry=dry,
        default=default
    )

    p, m, f = find_project_files(os.getcwd())

    ctx.obj['path'] = p
    ctx.obj['file'] = f
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
@click.pass_context
def app(ctx, apps, is_auth):
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

    wrong_place_warning(ctx)

    try:
        project_name = ctx.obj['project_name']
    except TypeError:
        log_error(DEFAULT_MANAGEMENT_ERROR)
        raise click.Abort()

    auth_application = None

    try:
        os.chdir(ctx.obj['path'])
    except TypeError:
        log_error(DEFAULT_MANAGEMENT_ERROR)
        raise click.Abort()

    if is_auth:
        auth_application = click.prompt(f"Which app will be used for authentication? {apps}")
        while auth_application not in apps:
            auth_application = click.prompt(f"Please choose a valid option: {apps}")

    helper = ctx.obj['helper']

    for name in apps:
        is_custom_app = (name == auth_application)

        helper.create_app(
            project=project_name,
            app=name,
            auth=is_custom_app
        )
