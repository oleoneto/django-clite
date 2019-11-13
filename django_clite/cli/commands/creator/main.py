import click
import os
from .helper import CreatorHelper
from django_clite.cli import (
    log_error,
    log_info,
    find_management_file,
    sanitized_string
)

DEFAULT_MANAGEMENT_ERROR = """The CLI could not decipher your django project.
Please try to create your app inside a Django project directory.
"""

DEFAULT_MANAGEMENT_TIP = """Tip:
If your project is called `website`, for example, 
you need to run `D new app app_name` from within `website` or `website/website`.
"""


def wrong_place_warning(ctx):
    if ctx.obj['path']:
        return False
    return True


@click.group()
@click.pass_context
@click.option('--dry', is_flag=True, help="Display output without creating files.")
def create(ctx, dry):
    """
    Creates projects and apps.
    """
    ctx.ensure_object(dict)

    p, m, c, f = find_management_file(os.getcwd())

    ctx.obj['dry'] = dry
    ctx.obj['cwd'] = os.getcwd()
    ctx.obj['path'] = p
    ctx.obj['management'] = m
    ctx.obj['code'] = c


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
    helper = CreatorHelper()

    if not ctx.obj['dry']:
        helper.create_project(
            project=name,
            apps=apps,
            docker=docker,
            dokku=dokku,
            dry=ctx.obj['dry']
        )
        if custom_auth:
            os.chdir(sanitized_string(name))
            ctx.obj['path'] = os.getcwd()
            ctx.invoke(app, apps=['authentication'], custom_auth=True)


@create.command()
@click.argument('apps', nargs=-1)
@click.option('--custom-auth', is_flag=True, help="Add User for custom authentication.")
@click.pass_context
def app(ctx, apps, custom_auth):
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
    helper = CreatorHelper()

    will_create_app = True

    if not ctx.obj['path']:
        log_error(DEFAULT_MANAGEMENT_ERROR)
        log_info(DEFAULT_MANAGEMENT_TIP)
        will_create_app = False

    if will_create_app:

        if not ctx.obj['dry']:
            path = ctx.obj['path']
            project_name = ctx.obj['path'].rsplit('/')[-1]

            os.chdir(path)
            for app_name in apps:
                helper.create_app(
                    app_name=app_name,
                    project=project_name,
                    dry=ctx.obj['dry'],
                    custom_auth=custom_auth
                )
