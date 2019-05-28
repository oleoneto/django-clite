import click
from djangle.cli import log_error
from .helpers.base import DestroyHelper
from djangle.cli.templates.admin import model_admin_import
from djangle.cli.templates.model import modelImportTemplate
from djangle.cli.templates.viewset import ViewSetImportTemplate


def not_an_app_directory_warning(ctx):
    if not ctx.obj['in_app']:
        log_error("Not inside an app directory")
        exit(1)


def confirm_delete():
    return click.confirm(ctx.obj['warning'], show_default=True, default=False)


@click.group()
@click.option('--dry', is_flag=True, help="Display output without deleting files")
@click.pass_context
def destroy(ctx, dry):
    """
    Removes models, serializers, and other resources
    """
    ctx.ensure_object(dict)
    ctx.obj['dry'] = dry
    ctx.obj['in_app'] = 'apps.py' in os.listdir('.')
    ctx.obj['cwd'] = os.getcwd()
    ctx.obj['warning'] = "Are you sure you want to destroy the resource?"


@destroy.command()
@click.argument('name')
@click.option('--inline', is_flag=True, help='Destroy inline admin model')
def admin(ctx, name, inline):
    """
    Destroys an admin model under /admin
    """

    not_an_app_directory_warning(ctx)

    # Default admins directory
    base_dir = f"{ctx.obj['cwd']}/admin/"

    # Default helper
    helper = DestroyHelper()

    if confirm_delete():
        helper.destroy(path=base_dir, model=name, template=model_admin_import)


@destroy.command()
@click.argument('name')
@click.pass_context
def model(ctx, name):
    """
    Destroys a model under /models
    """

    not_an_app_directory_warning(ctx)

    # Default models directory
    base_dir = f"{ctx.obj['cwd']}/models/"

    # Default helper
    helper = DestroyHelper()

    # TODO: handle models registered in admin.site
    if confirm_delete():
        helper.destroy(path=base_dir, model=name, template=modelImportTemplate)


@destroy.command()
@click.argument('name')
@click.pass_context
def viewset(ctx, name):
    """
    Destroys a viewset under /viewsets
    """

    not_an_app_directory_warning(ctx)

    # Default viewsets directory
    base_dir = f"{ctx.obj['cwd']}/viewsets/"

    # Default helper
    helper = DestroyHelper()

    if confirm_delete():
        helper.destroy(path=base_dir, model=name, template=ViewSetImportTemplate)


@destroy.command()
@click.argument('name')
@click.pass_context
def serializer(ctx, name):
    """
    Destroys a serializer under /serializers
    """

    not_an_app_directory_warning(ctx)

    # Default serializer directory
    base_dir = f"{ctx.obj['cwd']}/serializers/"

    # Default helper
    helper = DestroyHelper()

    # TODO: fix deletion
    # TODO: handle viewsets that depend on this serializer
    if confirm_delete():
        helper.destroy(path=base_dir, model=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def form(ctx, name):
    """
    Destroys a form under /forms
    """

    not_an_app_directory_warning(ctx)

    # Default forms directory
    base_dir = f"{ctx.obj['cwd']}/forms/"

    # Default helper
    helper = DestroyHelper()

    # TODO: fix deletion
    if confirm_delete():
        helper.destroy(path=base_dir, model=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def template(ctx, name):
    """
    Destroys a form under /templates
    """

    not_an_app_directory_warning(ctx)

    # Default forms directory
    base_dir = f"{ctx.obj['cwd']}/templates/"

    # Default helper
    helper = DestroyHelper()

    # Resource to be destroyed
    resource = f"{name.lower()}.html"

    # TODO: fix deletion
    if confirm_delete():
        helper.delete(path=base_dir, model=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def view(ctx, name):
    """
    Destroys a form under /views
    """

    not_an_app_directory_warning(ctx)

    # Default forms directory
    base_dir = f"{ctx.obj['cwd']}/views/"

    # Default helper
    helper = DestroyHelper()

    # TODO: fix deletion
    if confirm_delete():
        helper.delete(path=base_dir, model=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def resource(ctx, name):
    """
    Destroys scaffold resources
    """

    not_an_app_directory_warning(ctx)
