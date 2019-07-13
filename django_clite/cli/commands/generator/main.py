import click
import os
from django_clite.cli import log_error
from .helpers import (
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


@click.group()
@click.option('--dry', is_flag=True, help="Display output without creating files.")
@click.pass_context
def generate(ctx, dry):
    """
    Adds models, routes, and other resources
    """
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


@generate.command()
@click.argument('name')
@click.option('--inline', is_flag=True, help='Register admin model as inline.')
@click.pass_context
def admin(ctx, name, inline):
    """
    Generates an admin model within the admin package.
    """

    # Default helper
    helper = AdminHelper()

    path = ctx.obj['admin']

    if inline:
        path = ctx.obj['admin_inlines']

    helper.create(model=name, inline=inline, path=path, dry=ctx.obj['dry'])


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def form(ctx, name):
    """
    Generates a model form within the forms package.
    """

    # Default helper
    helper = FormHelper()

    path = ctx.obj['forms']

    helper.create(model=name, path=path, dry=ctx.obj['dry'])


@generate.command()
@click.argument("name", required=True)
@click.argument("fields", nargs=-1, required=False)
@click.option('--abstract', is_flag=True, help="Creates an abstract model type.")
@click.option('--register-admin', is_flag=True, help="Register model to admin site.")
@click.option('--register-inline', is_flag=True, help="Register model to admin site as inline.")
@click.option('--test-case', is_flag=True, help="Creates a TestCase for model.")
@click.option('--full', is_flag=True, help="Adds admin, inline, and TestCase")
@click.pass_context
def model(ctx, name, full, abstract, fields, register_admin, register_inline, test_case):
    """
    Generates a model under the models directory.
    One can specify multiple attributes after the model's name, like so:

        D g model track int:number char:title fk:album bool:is_favorite

    This will generate a Track model and add a foreign key of Album.
    If the model is to be added to admin.site one can optionally opt in by specifying the --register-admin flag.
    """

    # Default helper
    helper = ModelHelper()

    path = ctx.obj['models']

    helper.create(
        model=name,
        abstract=abstract,
        fields=fields,
        path=path,
        dry=ctx.obj['dry']
    )

    if register_admin or full:
        ctx.invoke(admin, name=name)

    if register_inline or full:
        ctx.invoke(admin, name=name, inline=True)

    if test_case or full:
        ctx.invoke(test, model=name)


@generate.command()
@click.argument("name", required=True)
@click.argument("fields", nargs=-1)
@click.pass_context
def resource(ctx, name, fields):
    """
    Fully implements an app resource.

    This is ideal to add a model along with admin, serializer, view, viewset, template, and tests.
    You can invoke this command the same way you would the model command:

        D g resource track int:number char:title fk:album bool:is_featured

    This will generate a model with the specified attributes and all the related modules specified above.
    """

    ctx.invoke(
        model,
        name=name,
        register_admin=True,
        register_inline=True,
        fields=fields,
        test_case=True
    )

    ctx.invoke(serializer, name=name)

    ctx.invoke(viewset, name=name)

    ctx.invoke(form, name=name)

    ctx.invoke(template, name=name)

    ctx.invoke(view, name=name, list=True)


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def serializer(ctx, name):
    """
    Generates a serializer for a given model.

    Checks for the existence of the specified model in models.py
    before attempting to create a serializer for it. Aborts if model is not found.
    """

    # Default helper
    helper = SerializerHelper()

    path = ctx.obj['serializers']

    helper.create(model=name, path=path, dry=ctx.obj['dry'])


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def template(ctx, name):
    """
    Generates an html template.
    """

    # Default helper
    helper = TemplateHelper()

    path = ctx.obj['templates']

    helper.create(name=name, path=path, dry=ctx.obj['dry'])


@generate.command()
@click.argument("model", required=True)
@click.pass_context
def test(ctx, model):
    """
    Generates a new TestCase.
    """

    # Default helper
    helper = TestHelper()

    path = ctx.obj['tests']

    helper.create(
        model=model,
        path=path,
        dry=ctx.obj['dry']
    )


@generate.command()
@click.argument("name", required=True)
@click.option('--list', is_flag=True, help="Create model list view.")
@click.option('--detail', is_flag=True, help="Create model detail view.")
@click.pass_context
def view(ctx, name, list, detail):
    """
    Generates a view function or class.
    """

    # Default helper
    helper = ViewHelper()

    path = ctx.obj['views']

    helper.create(
        model=name,
        name=name,
        detail=detail,
        list=list,
        path=path,
        dry=ctx.obj['dry']
    )


@generate.command()
@click.option('--read-only', is_flag=True, help="Create a read-only viewset.")
@click.argument("name", required=True)
@click.pass_context
def viewset(ctx, read_only, name):
    """
    Generates a viewset for a serializable model.
    """

    # Default helper
    helper = ViewSetHelper()

    path = ctx.obj['viewsets']

    helper.create(model=name, path=path, read_only=read_only, dry=ctx.obj['dry'])
