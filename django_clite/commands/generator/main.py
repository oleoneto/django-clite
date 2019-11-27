import os
import click
from .helpers import *
from django_clite.helpers.logger import log_error, log_standard
from django_clite.helpers import get_project_name
from django_clite.helpers import find_project_files


def not_an_app_directory_warning():
    if not ('apps.py' in os.listdir('.')):
        log_error("Not inside an app directory")
        raise click.Abort


@click.group()
@click.option('--dry', is_flag=True, help="Display output without creating files.")
@click.option('--force', is_flag=True, help="Override any conflicting files.")
@click.pass_context
def generate(ctx, dry, force):
    """
    Adds models, routes, and other resources
    """
    not_an_app_directory_warning()

    ctx.ensure_object(dict)

    p, m, f = find_project_files(os.getcwd())

    ctx.obj['dry'] = dry
    ctx.obj['force'] = force
    ctx.obj['in_app'] = 'apps.py' in os.listdir('.')
    ctx.obj['cwd'] = os.getcwd()
    ctx.obj['admin'] = f"{os.getcwd()}/admin/"
    ctx.obj['admin_inlines'] = f"{os.getcwd()}/admin/inlines/"
    ctx.obj['forms'] = f"{os.getcwd()}/forms/"
    ctx.obj['migrations'] = f"{os.getcwd()}/migrations/"
    ctx.obj['models'] = f"{os.getcwd()}/models/"
    ctx.obj['models_tests'] = f"{os.getcwd()}/models/tests/"
    ctx.obj['managers'] = f"{os.getcwd()}/models/managers"
    ctx.obj['serializers'] = f"{os.getcwd()}/serializers/"
    ctx.obj['serializers_tests'] = f"{os.getcwd()}/serializers/tests/"
    ctx.obj['tests'] = f"{os.getcwd()}/tests/"
    ctx.obj['templates'] = f"{os.getcwd()}/templates/"
    ctx.obj['views'] = f"{os.getcwd()}/views/"
    ctx.obj['viewsets'] = f"{os.getcwd()}/viewsets/"

    if f is not None:
        ctx.obj['project_name'] = get_project_name(f)
    else:
        ctx.obj['project_name'] = None


@generate.command()
@click.argument('name')
@click.option('--inline', is_flag=True, help='Register admin model as inline.')
@click.pass_context
def admin(ctx, name, inline):
    """
    Generates an admin model within the admin package.
    """

    path = ctx.obj['admin']

    if inline:
        path = ctx.obj['admin_inlines']

    helper = AdminHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force']
    )

    helper.create(model=name, inline=inline)


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def form(ctx, name):
    """
    Generates a model form within the forms package.
    """

    path = ctx.obj['forms']

    helper = FormHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force']
    )

    helper.create(model=name)


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def manager(ctx, name):
    """
    Generates a model manager under the model managers directory.
    """
    path = ctx.obj['managers']

    helper = ManagerHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force']
    )

    helper.create(model=name)


@generate.command()
@click.option('-a', '--abstract', is_flag=True, help="Creates an abstract model type.")
@click.option('-t', '--test-case', is_flag=True, help="Creates a TestCase for model.")
@click.option('-v', '--view', is_flag=True, help="Make model an SQL view.")
@click.option('-f', '--full', is_flag=True, help="Adds all related resources and TestCase")
@click.option('--register-admin', is_flag=True, help="Register model to admin site.")
@click.option('--register-inline', is_flag=True, help="Register model to admin site as inline.")
@click.option('-i', '--inherits', required=False, help="Add model inheritance.")
@click.option('--app', required=False, help="If base model inherits is in another app.")
@click.argument("name", required=True)
@click.argument("fields", nargs=-1, required=False)
@click.pass_context
def model(ctx, name, full, abstract, fields, register_admin, register_inline, test_case, inherits, app, view):
    """
    Generates a model under the models directory.
    One can specify multiple attributes after the model's name, like so:

        D g model track int:number char:title fk:album bool:is_favorite

    This will generate a Track model and add a foreign key of Album.
    If the model is to be added to admin.site one can optionally opt in by specifying the --register-admin flag.
    """

    # Ensure --app is used only if --inherits is used
    if app and not inherits:
        log_error("You've specified an app inheritance scope but did not specify the model to inherit from.")
        log_error("Please rerun the command like so:")
        log_standard(f"D generate model {name} --inherits BASE_MODEL --app {app}")
        raise click.Abort

    path = ctx.obj['models']

    helper = ModelHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
    )

    helper.create(
        model=name,
        abstract=abstract,
        fields=fields,
        inherits=inherits,
        scope=app,
        project=ctx.obj['project_name'],
        view=view
    )

    if register_admin or full:
        ctx.invoke(admin, name=name)

    if register_inline or full:
        ctx.invoke(admin, name=name, inline=True)

    if test_case or full:
        ctx.invoke(test, name=name, scope="model")

    if full:
        ctx.invoke(form, name=name)
        ctx.invoke(serializer, name=name)
        ctx.invoke(template, name=name)
        ctx.invoke(view, name=name, list=True)
        ctx.invoke(view, name=name, detail=True)
        ctx.invoke(viewset, name=name)


@generate.command()
@click.argument("name", required=True)
@click.argument("fields", nargs=-1)
@click.option('-i', '--inherits', required=False, help="Add model inheritance.")
@click.option('--api', is_flag=True, help='Only add api-related files.')
@click.pass_context
def resource(ctx, name, fields, inherits, api):
    """
    Generates an app resource.

    This is ideal to add a model along with admin, serializer, view, viewset, template, and tests.
    You can invoke this command the same way you would the model command:

        D g resource track int:number char:title fk:album bool:is_featured

    This will generate a model with the specified attributes and all the related modules specified above.

    In case you're building an api, and don't need forms, templates and views, you can pass the --api flag to the command
    in order to prevent these files from being created.
    """

    ctx.invoke(
        model,
        name=name,
        register_admin=True,
        register_inline=True,
        fields=fields,
        test_case=True,
        inherits=inherits
    )

    ctx.invoke(serializer, name=name)

    ctx.invoke(viewset, name=name)

    if not api:
        ctx.invoke(form, name=name)
        ctx.invoke(template, name=name)
        ctx.invoke(view, name=name, class_type='list')


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def serializer(ctx, name):
    """
    Generates a serializer for a given model.

    Checks for the existence of the specified model in models.py
    before attempting to create a serializer for it. Aborts if model is not found.
    """

    path = ctx.obj['serializers']

    helper = SerializerHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force']
    )

    helper.create(model=name)

    ctx.invoke(test, name=name, scope='serializer')


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def template(ctx, name):
    """
    Generates an html template.
    """

    path = ctx.obj['templates']

    helper = TemplateHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force']
    )

    helper.create(model=name)


@generate.command()
@click.argument("name", required=True)
@click.option("-s", "--scope", type=click.Choice(['model', 'serializer']), required=True)
@click.pass_context
def test(ctx, name, scope):
    """
    Generates a new TestCase.
    """

    # TODO: Find better way to deal with scope
    path = ctx.obj[f'{scope}s_tests']

    helper = TestHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force']
    )

    helper.create(model=name, scope=scope)


@generate.command()
@click.argument("name", required=True)
@click.option("-c", "--class-type", type=click.Choice(['list', 'detail']))
@click.option('-t', is_flag=True, help='Generate related template.')
@click.pass_context
def view(ctx, name, class_type, t):
    """
    Generates a view function or class.
    """

    path = ctx.obj['views']

    helper = ViewHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force']
    )

    helper.create(model=name, class_type=class_type)

    if t:
        ctx.invoke(template, name=name)


@generate.command()
@click.option('-r', '--read-only', is_flag=True, help="Create a read-only viewset.")
@click.argument("name", required=True)
@click.pass_context
def viewset(ctx, read_only, name):
    """
    Generates a viewset for a serializable model.
    """

    path = ctx.obj['viewsets']

    helper = ViewSetHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force']
    )

    helper.create(
        model=name,
        read_only=read_only
    )


# @generate.command()
@click.option('-s', '--source', is_flag=True, help="Base table for SQL view.")
@click.argument("name", required=True)
@click.argument("fields", nargs=-1, required=False)
@click.pass_context
def sql_view(ctx, name, fields, source):
    """
    Generates a model as an SQL view.
    One can specify multiple attributes after the model's name, like so:

        D g sql_view track int:number char:title --source app_tracks
    """

    path = ctx.obj['models']

    helper = ModelHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force']
    )

    helper.create(
        model=name,
        is_sql=True,
        source=source,
        abstract=False,
        inherits=None,
        fields=fields,
    )
