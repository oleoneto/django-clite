import click
import os
from cli.helpers import get_project_name
from cli.helpers import find_project_files
from cli.helpers import not_in_project
from cli.helpers import wrong_place_warning
from cli.helpers.logger import *
from cli.commands.inspect.main import InspectorHelper
from cli.commands.inspect.main import inspect
from cli.commands.create.helpers.app import AppHelper
from cli.commands.create.helpers.creator import CreatorHelper
from cli.commands.create.helpers import inquire_app_presets
from cli.commands.create.helpers import inquire_docker_options
from cli.commands.create.helpers import inquire_project_presets
# from cli.commands.create.helpers import inquire_installable_apps


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
    ctx.obj['project'] = get_project_name(f)


@create.command(name='project')
@click.argument('name')
@click.argument('apps', nargs=-1)
@click.option('--defaults', is_flag=True, help="Apply defaults to project")
@click.pass_context
def create_project(ctx, name, apps, defaults):
    """
    Creates a new django project.

    This is similar to using `django-admin startproject project_name` but with some added functionality.
    The command can handle the creation of apps upon creation of any project, you can simply specify the name of
    the apps after the project name:

        D new project website app1 app2 app3 ...
    """

    try:
        helper = ctx.obj['helper']

        # project presets
        presets = inquire_project_presets(project_name=name, default=defaults)
    
        # project app settings
        # settings_apps, settings_middleware = inquire_installable_apps(default=defaults)
    
        # docker settings
        services = {} if 'dockerized' not in presets['presets'] else inquire_docker_options(default=defaults)

        # Create project
        helper.create_project(
            project=name,
            apps=apps,
            **presets,
            **services,
            # settings_apps=settings_apps,
            # settings_middleware=settings_middleware,
        )

        # Add info to .cli_config.json
        helper.write_cli_config()

        # apps = ctx.invoke(inspect, scope='apps', no_stdout=True)
        # resources = ctx.invoke(inspect, scope='models', no_stdout=True)
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        log_error(f'Exited! {repr(e)}')


@create.command(name='apps')
@click.argument('apps', nargs=-1)
@click.option('--project', '-p', help="Specify name of your project.")
@click.option('--package', is_flag=True, help="Specify that the app can be installed as a package.")
@click.option('--directory', '-d', type=click.Path(), help="Specify path to your project's management file.")
@click.option('--api', is_flag=True, help="Add a special api urls module to your app directory.")
@click.option('--defaults', is_flag=True, help="Apply defaults to project")
@click.pass_context
def create_applications(ctx, apps, project, package, directory, api, defaults):
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

    As part of the CLI convention, each app is assigned its own `urls.py` file, which can be used to route urls on a
    per app basis. Another convention the CLI adopts is
    to add a viewsets package to the app's directory by default (for use with DRF). Within the viewsets directory
    a DRF router is instantiated in `router.py` and its urls added to each app's urlpatterns by default.
    """

    try:
        # Get project name from arguments
        project = project if project else ctx.obj['project']
        directory = directory if directory else ctx.obj['management']
    
        if not_in_project(ctx) and not package:
            if not click.confirm(DEFAULT_MANAGEMENT_APP_ERROR_PROMPT):
                return False
    
        helper = AppHelper(
            cwd=os.getcwd(),
            dry=ctx.obj['dry'],
            verbose=ctx.obj['verbose'],
            package=package,
        )
    
        options = {}
        if len(apps) == 1:
            if package:
                options = inquire_app_presets(apps[0], default=defaults)
    
        for name in apps:
            helper.create_app(
                project=project,
                app=name,
                api=api,
                **options,
            )
    
            click.echo(f"Successfully created app: {name}")

        print(helper.config)
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        log_error('Exited!')


@create.command(name='settings')
@click.option('--ignore-apps', is_flag=True, help="Do not add project apps to INSTALLED_APPS.")
@click.option('--override-file', is_flag=True, help="Override contents of current settings.py module")
@click.pass_context
def create_settings(ctx, ignore_apps, override_file):
    """
    Create settings file for project.
    """

    try:
        wrong_place_warning(ctx)
        project_name = ctx.obj['project']
        path = os.path.join(ctx.obj['management'], project_name)

        helper = ctx.obj['helper']
    
        if not ignore_apps:
            ctx.obj['helper'] = InspectorHelper(cwd=ctx.obj['management'])
            apps = ctx.invoke(inspect, scope='apps', suppress_output=True)
            helper.create_file_in_context(
                project=ctx.obj['project'],
                template='settings.tpl',
                filename='settings_override.py',
                apps=apps
            )
        else:
            helper.create_file_in_context(
                project=ctx.obj['project'],
                template='settings.tpl',
                filename='settings_override.py',
            )
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        log_error(f'Exited! {repr(e)}')
