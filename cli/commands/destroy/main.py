import click
from cli.helpers import add_app_package_paths_to_context
from cli.helpers import ensure_test_directory
from cli.helpers import not_an_app_directory_warning
from cli.commands.generate.helpers import AdminHelper
from cli.commands.generate.helpers import FixtureHelper
from cli.commands.generate.helpers import FormHelper
from cli.commands.generate.helpers import ManagerHelper
from cli.commands.generate.helpers import ModelHelper
from cli.commands.generate.helpers import SerializerHelper
from cli.commands.generate.helpers import SignalHelper
from cli.commands.generate.helpers import TemplateHelper
from cli.commands.generate.helpers import TemplateTagHelper
from cli.commands.generate.helpers import TestHelper
from cli.commands.generate.helpers import ViewHelper
from cli.commands.generate.helpers import ViewSetHelper


SUPPORTED_VIEW_TYPES = ['create', 'detail', 'list', 'update']


@click.group()
@click.pass_context
def destroy(ctx):
    """
    Removes models, serializers, and other resources
    """
    if not ctx.obj['dry']:
        not_an_app_directory_warning()

    ctx.ensure_object(dict)

    add_app_package_paths_to_context(context=ctx)


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

    name = ModelHelper.check_noun(name)

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
        ctx.invoke(template, name=name, class_type='list')
        ctx.invoke(template, name=name, class_type='detail')
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

    name = ModelHelper.check_noun(name)

    ctx.invoke(admin, name=name)
    ctx.invoke(admin, name=name, inline=True)

    ctx.invoke(form, name=name)

    ctx.invoke(
        model,
        name=name,
        unregister_admin=True,
        unregister_inline=True,
        test_case=True
    )

    ctx.invoke(serializer, name=name)

    ctx.invoke(view, name=name, class_type='list')
    ctx.invoke(view, name=name, class_type='detail')
    ctx.invoke(view, name=name)

    ctx.invoke(viewset, name=name)


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
@click.argument("name", required=True)
@click.pass_context
def signal(ctx, name):
    """
    Generates a signal.
    """

    path = ctx.obj['signals']

    helper = TemplateTagHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose'],
    )

    helper.delete(name=name)


@destroy.command()
@click.argument('name')
@click.option("-c", "--class-type", type=click.Choice(SUPPORTED_VIEW_TYPES))
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

    ctx.invoke(template, name=name, class_type=class_type)

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
@click.option("-c", "--class-type", type=click.Choice(SUPPORTED_VIEW_TYPES))
@click.pass_context
def template(ctx, name, class_type):
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

    h.delete(model=name, class_type=class_type)


@destroy.command(name='tag')
@click.argument("name", required=True)
@click.pass_context
def templatetag(ctx, name):
    """
    Destroys a template tag.
    """

    path = ctx.obj['templatetags']

    helper = TemplateTagHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose'],
    )

    helper.delete(name=name)


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
