import click
import os
from djangle.cli import log_error
from djangle.cli.commands.generator.helpers import (
    AdminHelper,
    FormHelper,
    ModelHelper,
    SerializerHelper,
    TemplateHelper,
    TestHelper,
    ViewHelper,
    ViewSetHelper
)


def not_an_app_directory_warning(ctx):
    if not ctx.obj['in_app']:
        log_error("Not inside an app directory")
        raise click.Abort


def confirm_delete():
    return click.confirm("Are you sure you want to delete this file?", show_default=True, default=False)


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
    ctx.obj['admin'] = f"{os.getcwd()}/admin/"
    ctx.obj['admin_inlines'] = f"{os.getcwd()}/admin/inlines/"
    ctx.obj['forms'] = f"{os.getcwd()}/forms/"
    ctx.obj['models'] = f"{os.getcwd()}/models/"
    ctx.obj['serializers'] = f"{os.getcwd()}/serializers/"
    ctx.obj['tests'] = f"{os.getcwd()}/tests/"
    ctx.obj['templates'] = f"{os.getcwd()}/templates/"
    ctx.obj['views'] = f"{os.getcwd()}/views/"
    ctx.obj['viewsets'] = f"{os.getcwd()}/viewsets/"


@destroy.command()
@click.argument('name')
@click.option('--inline', is_flag=True, help='Destroy inline admin model')
@click.pass_context
def admin(ctx, name, inline):
    """
    Destroys an admin model or inline
    """

    not_an_app_directory_warning(ctx)

    # Default helper
    helper = AdminHelper()

    path = ctx.obj['admin']

    if inline:
        path = ctx.obj['admin_inlines']

    if confirm_delete():
        helper.delete(model=name, path=path, inline=inline, dry=ctx.obj['dry'])


@destroy.command()
@click.argument('name', required=True)
@click.pass_context
def form(ctx, name):
    """
    Destroys a form
    """

    not_an_app_directory_warning(ctx)

    # Default forms directory
    path = ctx.obj['forms']

    # Default helper
    helper = FormHelper()

    # TODO: fix deletion
    if confirm_delete():
        helper.delete(path=path, model=name)


@destroy.command()
@click.argument('name')
@click.option('--unregister-admin', is_flag=True, help="Unregister model from the admin site.")
@click.option('--unregister-inline', is_flag=True, help="Unregister inline model from the admin site.")
@click.option('--test-case', is_flag=True, help="Delete TestCases for model.")
@click.option('--full', is_flag=True, help="Delete admin, inline, and TestCase")
@click.pass_context
def model(ctx, name, full, unregister_admin, unregister_inline, test_case):
    """
    Destroys a model
    """

    not_an_app_directory_warning(ctx)

    # Default models directory
    path = ctx.obj['models']

    # Default helper
    helper = ModelHelper()

    # TODO: handle models registered in admin.site
    if confirm_delete():
        helper.delete(
            model=name,
            path=path,
            dry=ctx.obj['dry']
        )

        if unregister_admin or full:
            ctx.invoke(admin, name=name)

        if unregister_inline or full:
            ctx.invoke(admin, name=name, inline=True)

        if test_case or full:
            ctx.invoke(test, model=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def resource(ctx, name):
    """
    Destroys resource
    """

    ctx.invoke(
        model,
        name=name,
        unregister_admin=True,
        unregister_inline=True,
        test_case=True
    )

    ctx.invoke(serializer, name=name)

    ctx.invoke(viewset, name=name)

    ctx.invoke(form, name=name)

    ctx.invoke(template, name=name)

    ctx.invoke(view, name=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def serializer(ctx, name):
    """
    Destroys a serializer
    """

    not_an_app_directory_warning(ctx)

    # Default serializer directory
    path = ctx.obj['serializers']

    # Default helper
    helper = SerializerHelper()

    # TODO: fix deletion
    # TODO: handle viewsets that depend on this serializer
    # if confirm_delete():
    #     helper.delete(path=path, model=name)


@destroy.command()
@click.argument('name')
@click.option('--list', is_flag=True, help='Deletes a model list view')
@click.option('--detail', is_flag=True, help='Deletes a model detail view')
@click.pass_context
def view(ctx, name, list, detail):
    """
    Destroys a view
    """

    not_an_app_directory_warning(ctx)

    # Default forms directory
    path = ctx.obj['views']

    # Default helper
    helper = ViewHelper()

    # TODO: fix deletion
    if confirm_delete():
        helper.delete(
            path=path,
            model=name,
            list=list,
            detail=detail,
            dry=ctx.obj['dry']
        )


@destroy.command()
@click.argument('name')
@click.pass_context
def viewset(ctx, name):
    """
    Destroys a viewset
    """

    not_an_app_directory_warning(ctx)

    # Default viewsets directory
    path = ctx.obj['viewsets']

    # Default helper
    helper = ViewSetHelper()

    # if confirm_delete():
    #     helper.delete(path=path, model=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def template(ctx, name):
    """
    Destroys a form under /templates
    """

    not_an_app_directory_warning(ctx)

    # Default forms directory
    path = ctx.obj['templates']

    # Default helper
    helper = TemplateHelper()

    # TODO: fix deletion
    # if confirm_delete():
    #     helper.delete(path=path, model=name)


@destroy.command()
@click.argument('model')
@click.pass_context
def test(ctx, model):
    """
    Destroys a TestCase.
    """

    not_an_app_directory_warning(ctx)

    # Default helper
    helper = TestHelper()

    path = ctx.obj['tests']

    helper.delete(
        model=model,
        path=path,
        dry=ctx.obj['dry']
    )
