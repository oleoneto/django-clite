import inflection
import click
from cli.utils.logger import Logger
from cli.utils.sanitize import sanitized_string, sanitized_string_callback
from cli.utils.sanitize import check_noun_inflection
from cli.handlers.parser.field_handler import parse_fields
from cli.commands.generate.helpers import resource_generator
from cli.commands.generate.admin import admin as register_admin
from cli.commands.generate.fixture import fixture
from cli.commands.generate.form import form as register_form
from cli.commands.generate.serializer import serializer
from cli.commands.generate.template import template
from cli.commands.generate.test import test
from cli.commands.generate.view import view
from cli.commands.generate.viewset import viewset


def fields_callback(ctx, _, value):
    fields, import_list = parse_fields(value, model=ctx.params['name'])
    return fields, import_list


def inheritance_callback(ctx, _, value):
    if value:
        value = sanitized_string(value)
        return {'name': value, 'classname': inflection.camelize(value)}
    return None


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.argument("fields", nargs=-1, required=False, callback=fields_callback)
@click.option('-a', '--abstract', is_flag=True, help="Creates an abstract model type")
@click.option('--api', is_flag=True, help="Adds only related api resources")
@click.option('--full', is_flag=True, help="Adds all related resources")
@click.option('--admin', is_flag=True, help='Register admin model')
@click.option('--fixtures', is_flag=True, help='Create model fixture')
@click.option('--form', is_flag=True, help='Create model form')
@click.option('--serializers', is_flag=True, help='Create serializers')
@click.option('--templates', is_flag=True, help='Create templates')
@click.option('--tests', is_flag=True, help='Create tests')
@click.option('--views', is_flag=True, help='Create views')
@click.option('--viewsets', is_flag=True, help='Create viewsets')
@click.pass_context
def model(ctx, name, fields, abstract, api, full, admin, fixtures, form, serializers, templates, tests, views, viewsets):
    """
    Generates a model under the models directory.
    One can specify multiple attributes after the model's name, like so:

        D g model track int:number char:title fk:album bool:is_favorite

    This will generate a Track model and add a foreign key of Album.
    If the model is to be added to admin.site one can optionally opt in by specifying the --register-admin flag.
    """

    name = check_noun_inflection(name)

    # Ensure --api and --full are not used simultaneously
    if api and full:
        Logger.log("Flags [b]--api[/b] and [b]--full[/b] cannot be used simultaneously.")
        raise click.Abort

    parsed_fields, import_list = fields

    resource_generator(
        name,
        template='model.tpl',
        package='models',
        import_context={'classname': inflection.camelize(name), 'name': name},
        context={
            'api': api,
            'abstract': abstract,
            'fields': parsed_fields,
            'import_list': import_list
        },
        **ctx.obj
    )

    pending = dict()

    if api:
        pending[serializer] = {'name': name}
        pending[viewset] = {'name': name}
        pending[test] = {'name': name, 'full': True}

    if full or admin:
        pending[register_admin] = {'name': name, 'fields': [f for f in parsed_fields if f.supported_in_admin]}

    if full or fixtures:
        pending[fixture] = {'name': name}

    if full or form:
        pending[register_form] = {'name': name}

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
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.argument("fields", nargs=-1, required=True, callback=fields_callback)
@click.option('--api', is_flag=True, help='Adds related api resources')
@click.pass_context
def resource(ctx, name, fields, api):
    """
    Generates an app resource.

    This is ideal to add a model along with admin, serializer, view, viewset, template, and tests.
    You can invoke this command the same way you would the model command:

        D g resource track int:number char:title fk:album bool:is_featured

    This will generate a model with the specified attributes and all the related modules specified above.

    In case you're building an api, and don't need forms, templates and views, you can pass the --api flag to the command
    in order to prevent these files from being created.
    """

    name = check_noun_inflection(name)

    try:
        ctx.invoke(model, name=name, fields=fields, api=api, full=not api)
    except (KeyboardInterrupt, SystemExit) as error:
        Logger.error(f'Exited! {error}')
