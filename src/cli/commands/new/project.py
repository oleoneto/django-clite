import click
from cli.utils import sanitized_string_callback
from .defaults.project import new_project
from .defaults.app import application_callback


@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.argument("apps", nargs=-1, callback=application_callback)
@click.option("--defaults", is_flag=True, help="Apply defaults to project.")
@click.pass_context
def project(ctx, name, apps, defaults):
    """
    Creates a new django project.

    This is similar to using `django-admin startproject project_name` but with some added functionality.
    The command can handle the creation of apps upon creation of any project, you can simply specify the name of
    the apps after the project name:

        django-clite new project website app1 app2 app3 ...
    """

    proj = new_project(name)

    proj.add_children(apps)

    proj.create()
