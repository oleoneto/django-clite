import click
from pathlib import Path
from django.core.management import call_command, CommandError
from django.core.management.commands import startproject

from .defaults.project import new_project, project_transformations
from .defaults.app import application_callback
from cli.commands.callbacks import sanitized_string_callback
from cli.constants import ENABLE_DRY_RUN_KEY
from cli.core.filesystem.filesystem import working_directory
from .app import apps as apps_cmd


@click.command()
@click.argument("name", callback=sanitized_string_callback)
@click.argument("apps", nargs=-1, callback=application_callback)
@click.option("--docker", is_flag=True, help="Render Dockerfile and other docker-related files.")
@click.option("--github", is_flag=True, help="Render GitHub CI template.")
@click.option("--kubernetes", is_flag=True, help="Render Kubernetes deployment files.")
# @click.option("--dokku", is_flag=True, help="Render Dokku deployment files.")
# @click.option("--heroku", is_flag=True, help="Render Heroku files.")
@click.pass_context
def project(ctx, name, apps, docker, github, kubernetes):  # TODO: dokku, heroku
    """
    Creates a new django project.

    This is similar to using `django-admin startproject project_name` but with some added functionality.
    The command can handle the creation of apps upon creation of any project, you can simply specify the name of
    the apps after the project name:

        django-clite new project myproject app1 app2 app3 ...
    """

    if ctx.obj[ENABLE_DRY_RUN_KEY]:
        return

    cmd = startproject.Command()

    try:
        call_command(cmd, name, verbosity=0)

        # Generate project files as per CLI conventions
        options = dict(ctx.params)
        options.pop("name")
        options.pop("apps")

        context = dict(ctx.obj)
        context.update({"project": name, "port": "8080", "workers": 1})

        proj = new_project(name, **options)
        proj.create(**context)

        dir_ = Path(name) / name  # i.e. myproject/myproject
        with working_directory(dir_):
            for t in project_transformations:
                # Customize django-generated files
                t.run()

        # Create nested apps
        with working_directory(name):
            ctx.invoke(apps_cmd, names=apps)

        # TODO: Initialize git repository?

    except CommandError as err:
        click.echo(
            f"Command returned an error {repr(err)}"
        )
        raise click.Abort()
