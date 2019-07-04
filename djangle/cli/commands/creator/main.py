import click
import subprocess
from .helper.create import CreatorHelper


@click.group()
@click.pass_context
@click.option('--dry', is_flag=True, help="Display output without creating files")
def new(ctx, dry):
    """
    Creates projects and apps
    """
    ctx.ensure_object(dict)
    ctx.obj['dry'] = dry


@new.command()
@click.argument('name')
@click.option('--docker', is_flag=True, help="Add support for Docker")
@click.option('--dokku', is_flag=True, help="Add support for Dokku")
@click.option('--core', is_flag=True, help="Add core app to project")
@click.argument('apps', nargs=-1)
@click.pass_context
def project(ctx, name, docker, dokku, core, apps):
    """
    Creates a new django project.
    \fThis is similar to using `django-admin startproject PROJECT_NAME`
    """
    helper = CreatorHelper()

    if apps:
        helper.create(project=name, apps=apps, nested=True, docker=docker, dokku=dokku, core=core)
    else:
        helper.create(project=name, docker=docker, dokku=dokku, core=core)


@new.command()
@click.argument('apps', nargs=-1)
@click.option('--nested', '-n', is_flag=True, help="Specify if app should be created one level below manage.py")
@click.pass_context
def app(ctx, apps, nested):
    """
    Creates a new django app.
    \fThis is similar to using `django-admin startapp APP_NAME`
    \fAlso adds models, viewsets, and serializers directories for better directory structure.
    """
    # TODO: Register new created app in INSTALLED_APPS
    helper = CreatorHelper()
    helper.create(apps=apps, nested=nested)
