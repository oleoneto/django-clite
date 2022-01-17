import click
import inflection
from cli.utils.logger import Logger
from cli.utils.sanitize import sanitized_string_callback
from cli.commands.destroy.helpers.resource_destroyer import resource_destroyer
from cli.commands.destroy.admin import admin as admin_
from cli.commands.destroy.form import form as form_
from cli.commands.destroy.fixture import fixture
from cli.commands.destroy.serializer import serializer
from cli.commands.destroy.template import template
from cli.commands.destroy.test import test
from cli.commands.destroy.view import view
from cli.commands.destroy.viewset import viewset


@click.command()
@click.argument('name', required=True, callback=sanitized_string_callback)
@click.option('--api', is_flag=True, help="Destroys only api-related resources")
@click.option('--full', is_flag=True, help="Destroy all related resources")
@click.option('--admin', is_flag=True, help='Destroy admin model')
@click.option('--fixtures', is_flag=True, help='Destroy model fixture')
@click.option('--form', is_flag=True, help='Destroy model form')
@click.option('--serializers', is_flag=True, help='Destroy serializers')
@click.option('--templates', is_flag=True, help='Destroy templates')
@click.option('--tests', is_flag=True, help='Destroy tests')
@click.option('--views', is_flag=True, help='Destroy views')
@click.option('--viewsets', is_flag=True, help='Destroy viewsets')
@click.pass_context
def model(ctx, name, api, full, admin, fixtures, form, serializers, templates, tests, views, viewsets):
    """
    Destroys a model.
    """

    # Ensure --api and --full are not used simultaneously
    if api and full:
        Logger.log("Flags [b]--api[/b] and [b]--full[/b] cannot be used simultaneously.")
        raise click.Abort

    resource_destroyer(
        name,
        package='models',
        import_context={'classname': inflection.camelize(name)},
        **ctx.obj
    )

    pending = dict()

    if api:
        pending[serializer] = {'name': name}
        pending[viewset] = {'name': name}
        pending[test] = {'name': name, 'full': True}

    if full or admin:
        pending[admin_] = {'name': name}

    if full or fixtures:
        pending[fixture] = {'name': name}

    if full or form:
        pending[form_] = {'name': name}

    if full or serializers:
        pending[serializer] = {'name': name}

    if full or templates:
        pending[template] = {'name': name, 'full': True}

    if full or tests:
        pending[test] = {'name': name, 'full': True}

    if full or views:
        pending[view] = {'name': name, 'full': True}

    if full or viewsets:
        pending[viewset] = {'name': name}

    # Create related resources

    for k, v in pending.items():
        ctx.invoke(k, **v)


@click.command()
@click.argument('name', required=True, callback=sanitized_string_callback)
@click.option('--api', is_flag=True, help='Only remove api-related resources')
@click.pass_context
def resource(ctx, name, api):
    """
    Destroys a resource and its related modules.
    """

    try:
        ctx.invoke(model, name=name, api=api, full=not api)
    except (KeyboardInterrupt, SystemExit) as error:
        Logger.error(f'Exited! {error}')


