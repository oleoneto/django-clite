import click

from .defaults.app import application_callback
from cli.constants import ENABLE_DRY_RUN_KEY


@click.command()
@click.argument("names", nargs=-1, callback=application_callback)
@click.option("--is-package", is_flag=True, help="Treat as a standalone Python package")
@click.pass_context
def apps(ctx, names, is_package):
    """
    Creates new django apps.

    This is similar to using `django-admin startapp app_name`
    but adds more structure to your app by creating packages for forms, models,
    serializers, tests, templates, views, and viewsets.

    The command can accept multiple apps as arguments. Like so:

        django-clite new apps shop blog forum

    The command above will create all 4 apps two levels within your project's
    directory, i.e. myproject/myproject. The CLI tries to identify where the management module for your
    project is, so it can place your app files in the correct location. This helps with consistency
    as the CLI can infer module/package scopes when performing other automatic configurations.

    As part of the CLI convention, each app is assigned its own `urls.py` file, which can be used to route urls on a
    per-app basis.
    Another convention the CLI adopts is to add a viewsets package to the app's directory by default (for use with DRF).
    Within the viewsets directory, a DRF router is instantiated in `router.py` and its urls added to each app's
    urlpatterns by default.
    """

    if ctx.obj[ENABLE_DRY_RUN_KEY]:
        return

    for application in names:
        context = dict(ctx.obj)
        context.update({"app": application.name})
        application.create(**context)
