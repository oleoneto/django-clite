import os
import click
from .helpers import *
from django_clite.helpers.logger import log_error


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
@click.option('--dry', '--dry-run', is_flag=True, help="Display output without deleting files")
@click.option('--force', is_flag=True, help="Override any conflicting files.")
@click.option('--verbose', is_flag=True, help="Run in verbose mode.")
@click.pass_context
def destroy(ctx, dry, force, verbose):
    """
    Removes models, serializers, and other resources
    """
    if not dry:
        not_an_app_directory_warning()

    ctx.ensure_object(dict)
    ctx.obj['dry'] = dry
    ctx.obj['force'] = force
    ctx.obj['verbose'] = verbose
    ctx.obj['in_app'] = 'apps.py' in os.listdir('.')
    ctx.obj['cwd'] = os.getcwd()
    ctx.obj['admin'] = f"{os.getcwd()}/admin/"
    ctx.obj['admin_inlines'] = f"{os.getcwd()}/admin/inlines/"
    ctx.obj['fixtures'] = f"{os.getcwd()}/fixtures/"
    ctx.obj['forms'] = f"{os.getcwd()}/forms/"
    ctx.obj['models'] = f"{os.getcwd()}/models/"
    ctx.obj['models_tests'] = f"{os.getcwd()}/models/tests/"
    ctx.obj['managers'] = f"{os.getcwd()}/models/managers/"
    ctx.obj['serializers'] = f"{os.getcwd()}/serializers/"
    ctx.obj['serializers_tests'] = f"{os.getcwd()}/serializers/tests/"
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
    Destroys an admin model or inline.
    """

    path = ctx.obj['admin']

    if inline:
        path = ctx.obj['admin_inlines']

    h = AdminHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    h.delete(model=name, inline=inline)


@destroy.command()
@click.argument('name')
@click.pass_context
def fixture(ctx, name):
    """
    Destroys a fixture.
    """

    path = ctx.obj.get('fixtures')

    helper = FixtureHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    helper.delete(model=name)


@destroy.command()
@click.argument('name', required=True)
@click.pass_context
def form(ctx, name):
    """
    Destroys a form.
    """

    path = ctx.obj['forms']

    h = FormHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    h.delete(model=name)


@destroy.command()
@click.argument('name', required=True)
@click.pass_context
def manager(ctx, name):
    """
    Destroys a model manager.
    """

    path = ctx.obj['managers']

    h = ManagerHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    h.delete(model=name)


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

    h = ModelHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    ensure_test_directory(path)

    h.delete(model=name)

    if unregister_admin or full:
        ctx.invoke(admin, name=name)

    if unregister_inline or full:
        ctx.invoke(admin, name=name, inline=True)

    if test_case or full:
        ctx.invoke(test, name=name, scope='model')

    if full:
        ctx.invoke(form, name=name)
        ctx.invoke(serializer, name=name)
        ctx.invoke(test, name=name, scope='serializer')
        ctx.invoke(template, name=name)
        ctx.invoke(view, name=name, class_type="list")
        ctx.invoke(view, name=name, class_type="detail")
        ctx.invoke(viewset, name=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def resource(ctx, name):
    """
    Destroys a resource and its related modules.
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

    if not ctx.invoke(view, name=name, class_type='list'):
        ctx.invoke(view, name=name, class_type='detail')
        ctx.invoke(view, name=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def serializer(ctx, name):
    """
    Destroys a serializer.
    """

    path = ctx.obj['serializers']

    h = SerializerHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    h.delete(model=name)
    
    ensure_test_directory(path)

    ctx.invoke(test, name=name, scope='serializer')


@destroy.command()
@click.argument('name')
@click.option("-c", "--class-type", type=click.Choice(['list', 'detail']))
@click.pass_context
def view(ctx, name, class_type):
    """
    Destroys a view.
    """

    path = ctx.obj['views']

    h = ViewHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    h.delete(model=name, class_type=class_type)


@destroy.command()
@click.argument('name')
@click.pass_context
def viewset(ctx, name):
    """
    Destroys a viewset.
    """

    path = ctx.obj['viewsets']

    h = ViewSetHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    h.delete(model=name)


@destroy.command()
@click.argument('name')
@click.pass_context
def template(ctx, name):
    """
    Destroys a template.
    """

    path = ctx.obj['templates']

    h = TemplateHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    h.delete(model=name)


@destroy.command()
@click.argument('name', required=True)
@click.option("-s", "--scope", type=click.Choice(['model', 'serializer']), required=True)
@click.pass_context
def test(ctx, name, scope):
    """
    Destroys a TestCase.
    """

    path = ctx.obj[f'{scope}s_tests']

    h = TestHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    ensure_test_directory(ctx.obj[f'{scope}s'])

    h.delete(model=name, scope=scope)
