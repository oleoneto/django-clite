import click
import os
from django_clite.cli import log_error
from django_clite.cli.commands.generator.helpers import (
    AdminHelper,
    FormHelper,
    ModelHelper,
    SerializerHelper,
    TemplateHelper,
    TestHelper,
    ViewHelper,
    ViewSetHelper
)


def not_an_app_directory_warning():
    if not ('apps.py' in os.listdir('.')):
        log_error("Not inside an app directory")
        raise click.Abort


def confirm_delete():
    if not click.confirm("Are you sure you want to delete this file?", show_default=True, default=False):
        raise click.Abort()
    return True


@click.group()
@click.option('--dry', '--dry-run', is_flag=True, help="Display output without deleting files")
@click.pass_context
def destroy(ctx, dry):
    """
    Removes models, serializers, and other resources
    """
    if not dry:
        not_an_app_directory_warning()

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
    ctx.obj['confirm'] = confirm_delete()


@destroy.command()
@click.argument('name')
@click.option('--inline', is_flag=True, help='Destroy inline admin model')
@click.pass_context
def admin(ctx, name, inline):
    """
    Destroys an admin model or inline.
    """

    # Default helper
    helper = AdminHelper()

    path = ctx.obj['admin']

    if inline:
        path = ctx.obj['admin_inlines']

    if ctx.obj['confirm']:
        helper.delete(
            model=name,
            path=path,
            inline=inline,
            dry=ctx.obj['dry']
        )


@destroy.command()
@click.argument('name', required=True)
@click.pass_context
def form(ctx, name):
    """
    Destroys a form.
    """

    path = ctx.obj['forms']

    # Default helper
    helper = FormHelper()

    if ctx.obj['confirm']:
        helper.delete(
            path=path,
            model=name,
            dry=ctx.obj['dry']
        )


@destroy.command()
@click.argument('name')
@click.option('--unregister-admin', is_flag=True, help="Unregister model from the admin site.")
@click.option('--unregister-inline', is_flag=True, help="Unregister inline model from the admin site.")
@click.option('--test-case', is_flag=True, help="Delete TestCases for model.")
@click.option('--full', is_flag=True, help="Delete admin, inline, and TestCase")
@click.pass_context
def model(ctx, name, full, unregister_admin, unregister_inline, test_case):
    """
    Destroys a model.
    """

    path = ctx.obj['models']

    # Default helper
    helper = ModelHelper()

    if ctx.obj['confirm']:
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
            ctx.invoke(test, name=name)

        if full:
            ctx.invoke(form, name=name)
            ctx.invoke(serializer, name=name)
            ctx.invoke(template, name=name)
            ctx.invoke(view, name=name, list=True)
            ctx.invoke(view, name=name, detail=True)
            ctx.invoke(viewset, name=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def resource(ctx, name):
    """
    Destroys a resource.
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
    Destroys a serializer.
    """

    path = ctx.obj['serializers']

    # Default helper
    helper = SerializerHelper()

    if ctx.obj['confirm']:
        helper.delete(
            path=path,
            model=name,
            dry=ctx.obj['dry']
        )


@destroy.command()
@click.argument('name')
@click.option('-l', '--list', is_flag=True, help='Deletes a model list view')
@click.option('-d', '--detail', is_flag=True, help='Deletes a model detail view')
@click.pass_context
def view(ctx, name, list, detail):
    """
    Destroys a view.
    """

    path = ctx.obj['views']

    # Default helper
    helper = ViewHelper()

    if ctx.obj['confirm']:
        helper.delete(
            path=path,
            model=name,
            name=name,
            list=list,
            detail=detail,
            dry=ctx.obj['dry']
        )


@destroy.command()
@click.argument('name')
@click.pass_context
def viewset(ctx, name):
    """
    Destroys a viewset.
    """

    path = ctx.obj['viewsets']

    # Default helper
    helper = ViewSetHelper()

    if ctx.obj['confirm']:
        helper.delete(
            path=path,
            model=name,
            dry=ctx.obj['dry']
        )


@destroy.command()
@click.argument('name')
@click.pass_context
def template(ctx, name):
    """
    Destroys a template.
    """

    path = ctx.obj['templates']

    # Default helper
    helper = TemplateHelper()

    if ctx.obj['confirm']:
        helper.delete(
            path=path,
            model=name,
            dry=ctx.obj['dry']
        )


@destroy.command()
@click.argument('name')
@click.pass_context
def test(ctx, name):
    """
    Destroys a TestCase.
    """

    # Default helper
    helper = TestHelper()

    path = ctx.obj['tests']

    if ctx.obj['confirm']:
        helper.delete(
            model=name,
            path=path,
            dry=ctx.obj['dry']
        )
