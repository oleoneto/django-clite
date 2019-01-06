import click
from .helpers.base import BaseHelper


@click.group()
@click.option('--dry', is_flag=True, help="Display output without deleting files")
@click.pass_context
def destroy(ctx, dry):
    """
    Removes models, serializers, and other resources
    """
    ctx.ensure_object(dict)
    ctx.obj['dry'] = dry
    ctx.obj['warning'] = "Are you sure you want to destroy the resource?"


@destroy.command()
@click.argument('name')
@click.pass_context
def form(ctx, name):
    """
    Destroys a form under /forms
    """

    # Default forms directory
    base_dir = 'app/forms/'

    # Default helper
    helper = BaseHelper()

    # Resource to be destroyed
    resource = f"{name.lower()}.py"

    if click.confirm(ctx.obj['warning'], show_default=True, default=False):
        helper.delete(base_dir, resource=resource)


@destroy.command()
@click.argument('name')
@click.pass_context
def model(ctx, name):
    """
    Destroys a model under /models
    """

    # Default models directory
    base_dir = 'app/models/'

    # TODO: handle models registered in admin.site
    # Default helper
    helper = BaseHelper()

    # Resource to be destroyed
    resource = f"{name.lower()}.py"

    if click.confirm(ctx.obj['warning'], show_default=True, default=False):
        helper.delete(base_dir, resource=resource)


@destroy.command()
@click.argument('name')
@click.pass_context
def viewset(ctx, name):
    """
    Destroys a viewset under /viewsets
    """

    # Default viewsets directory
    base_dir = 'app/viewsets/'

    # Default helper
    helper = BaseHelper()

    # Resource to be destroyed
    resource = f"{name.lower()}.py"

    if click.confirm(ctx.obj['warning'], show_default=True, default=False):
        helper.delete(base_dir, resource=resource)


@destroy.command()
@click.argument('name')
@click.pass_context
def serializer(ctx, name):
    """
    Destroys a serializer under /serializers
    """

    # Default serializer directory
    base_dir = 'app/serializers/'

    # TODO: handle viewsets that depend on this serializer
    # Default helper
    helper = BaseHelper()

    # Resource to be destroyed
    resource = f"{name.lower()}.py"

    if click.confirm(ctx.obj['warning'], show_default=True, default=False):
        helper.delete(base_dir, resource=resource)
