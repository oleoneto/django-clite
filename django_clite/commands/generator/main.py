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


def ensure_test_directory(cwd):
    if 'tests' in os.listdir(cwd):
        pass
    else:
        try:
            os.mkdir('tests')
        except FileExistsError:
            pass


@click.group()
@click.option('--dry', is_flag=True, help="Display output without creating files.")
@click.option('--force', is_flag=True, help="Override any conflicting files.")
@click.option('--verbose', is_flag=True, help="Run in verbose mode.")
@click.pass_context
def generate(ctx, dry, force, verbose):
    """
    Adds models, routes, and other resources
    """
    not_an_app_directory_warning()

    ctx.ensure_object(dict)

    p, m, f = find_project_files(os.getcwd())

    ctx.obj['dry'] = dry
    ctx.obj['force'] = force
    ctx.obj['verbose'] = verbose
    ctx.obj['in_app'] = 'apps.py' in os.listdir('.')
    ctx.obj['cwd'] = os.getcwd()
    ctx.obj['admin'] = f"{os.getcwd()}/admin/"
    ctx.obj['admin_inlines'] = f"{os.getcwd()}/admin/inlines/"
    ctx.obj['fixtures'] = f"{os.getcwd()}/fixtures/"
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
@click.option('--stub-permissions', is_flag=True, help='Add permission stubs to admin model.')
@click.argument("fields", nargs=-1, required=False)
@click.pass_context
def admin(ctx, name, inline, fields, stub_permissions):
    """
    Generates an admin model within the admin package.
    """

    path = ctx.obj['admin']

    fields = [f for f in fields]

    if inline:
        path = ctx.obj['admin_inlines']

    helper = AdminHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    helper.create(model=name, fields=fields, inline=inline, permissions=stub_permissions)


@generate.command()
@click.argument('name')
@click.argument("fields", nargs=-1, required=False)
@click.option('-n', '--number', default=1, help='Number of objects to create in fixture.')
@click.pass_context
def fixture(ctx, name, fields, number):
    """
    Generates model fixtures.
    """

    path = ctx.obj.get('fixtures')

    helper = FixtureHelper(
        cwd=path,
        dry=ctx.obj.get('dry'),
        force=ctx.obj.get('force'),
        verbose=ctx.obj.get('verbose')
    )

    helper.create(model=name, fields=fields, total=number)


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
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
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
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    helper.create(model=name)


@generate.command()
@click.option('-a', '--abstract', is_flag=True, help="Creates an abstract model type.")
@click.option('-t', '--test-case', is_flag=True, help="Creates a TestCase for model.")
@click.option('-f', '--full', is_flag=True, help="Adds all related resources and TestCase")
@click.option('--register-admin', is_flag=True, help="Register model to admin site.")
@click.option('--register-inline', is_flag=True, help="Register model to admin site as inline.")
@click.option('-m', '--is-managed', is_flag=True, help="Add created_by and updated_by fields.")
@click.option('-i', '--inherits', '--extends', required=False, help="Add model inheritance.")
@click.option('--app', required=False, help="If base model inherits is in another app.")
@click.option('--api', is_flag=True, help='Only add api-related files.')
@click.option('-s', '--soft-delete', is_flag=True, help='Add ability to soft-delete records.')
@click.argument("name", required=True)
@click.argument("fields", nargs=-1, required=False)
@click.pass_context
def model(ctx, name, full, abstract, fields, register_admin,
          register_inline, test_case, inherits, api, app, is_managed, soft_delete):
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
        verbose=ctx.obj['verbose']
    )

    ensure_test_directory(path)

    model_fields = helper.create(
        model=name,
        api=api,
        abstract=abstract,
        fields=fields,
        inherits=inherits,
        scope=app,
        project=ctx.obj['project_name'],
        is_managed=is_managed,
        soft_delete=soft_delete
    )

    if api:
        ctx.invoke(test, name=name, scope="model")
        ctx.invoke(serializer, name=name)
        ctx.invoke(viewset, name=name)

    if register_admin or full:
        ctx.invoke(admin, name=name, fields=model_fields)

    if register_inline or full:
        ctx.invoke(admin, name=name, inline=True)

    if (test_case or full) and not api:
        ctx.invoke(test, name=name, scope="model")

    if full and not api:
        ctx.invoke(serializer, name=name)
        ctx.invoke(viewset, name=name)

    if full:
        ctx.invoke(form, name=name)
        ctx.invoke(template, name=name)
        ctx.invoke(view, name=name, class_type="list")
        ctx.invoke(view, name=name, class_type="detail")

    # Retuning model fields
    return model_fields


@generate.command()
@click.argument("name", required=True)
@click.argument("fields", nargs=-1)
@click.option('-i', '--inherits', '--extends', required=False, help="Add model inheritance.")
@click.option('-m', '--is-managed', is_flag=True, help="Add created_by and updated_by fields.")
@click.option('--api', is_flag=True, help='Only add api-related files.')
@click.option('-s', '--soft-delete', is_flag=True, help='Add ability to soft-delete records.')
@click.pass_context
def resource(ctx, name, fields, inherits, api, is_managed, soft_delete):
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
        api=api,
        register_admin=api,
        register_inline=api,
        fields=fields,
        test_case=True,
        inherits=inherits,
        is_managed=is_managed,
        soft_delete=soft_delete
    )

    ctx.invoke(serializer, name=name)

    ctx.invoke(viewset, name=name)

    if not api:
        ctx.invoke(form, name=name)
        ctx.invoke(template, name=name)
        ctx.invoke(view, name=name, class_type='list', no_template=True)


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
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    helper.create(model=name)

    ensure_test_directory(path)

    ctx.invoke(test, name=name, scope='serializer')


@generate.command()
@click.argument("name", required=True)
@click.option("-c", "--class-type", type=click.Choice(['create', 'detail', 'list', 'edit', 'update']))
@click.pass_context
def template(ctx, name, class_type):
    """
    Generates an html template.
    """

    path = ctx.obj['templates']

    helper = TemplateHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    helper.create(model=name, class_type=class_type)


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
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    ensure_test_directory(ctx.obj[f'{scope}s'])

    helper.create(model=name, scope=scope)


@generate.command()
@click.argument("name", required=True)
@click.option("-c", "--class-type", type=click.Choice(['create', 'detail', 'list', 'edit', 'update']))
@click.option('--no-template', is_flag=True, default=False, help='Generate related template.')
@click.pass_context
def view(ctx, name, class_type, no_template):
    """
    Generates a view function or class.
    """

    path = ctx.obj['views']

    helper = ViewHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    class_type = 'form' if class_type == 'edit' else class_type

    helper.create(model=name, class_type=class_type)

    if no_template:
        pass
    else:
        ctx.invoke(template, name=name, class_type=class_type)


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
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
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
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    helper.create(
        model=name,
        is_sql=True,
        source=source,
        abstract=False,
        inherits=None,
        fields=fields,
    )
