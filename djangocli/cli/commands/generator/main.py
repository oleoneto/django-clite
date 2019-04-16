import click
import os
from djangocli.cli import log_error, log_success
from .helpers.model import ModelHelper
from .helpers.viewset import ViewSetHelper
from .helpers.serializer import SerializerHelper
from .helpers.form import FormHelper
from .helpers.template import TemplateHelper
from .helpers.admin import AdminHelper


def not_an_app_directory_warning(ctx):
    if not ctx.obj['in_app']:
        log_error("Not inside an app directory")
        exit(1)


@click.group()
@click.pass_context
@click.option('--dry', is_flag=True, help="Display output without creating files")
def generate(ctx, dry):
    """
    Adds models, routes, and other resources
    """
    ctx.ensure_object(dict)
    ctx.obj['dry'] = dry
    ctx.obj['in_app'] = 'apps.py' in os.listdir('.')


@generate.command()
@click.argument('name')
@click.option('--inline', is_flag=True, help='Register admin model as inline')
@click.pass_context
def admin(ctx, name, inline):
    """
    Generates an admin model within the admin directory.
    """

    not_an_app_directory_warning(ctx)

    # Default admin models directory
    base_dir = 'admin/'

    # Default helper
    helper = AdminHelper()

    if inline:
        base_dir = base_dir + 'inlines/'
        content = helper.create_inline(name=name)
    else:
        # Create content for file
        content = helper.create(name=name)

    # Handling --dry flag
    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        file = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=file, file_content=content)
            log_success(f"Created admin model {name.capitalize()} in {file}")
            helper.create_in_init(path=base_dir, name=name)
        except FileExistsError:
            log_error(f"File {name} already exists")
            return


@generate.command()
@click.option('--admin', is_flag=True, help="Register model to admin site")
@click.option('--abstract', is_flag=True, help="Creates an abstract model type")
@click.option('--no-defaults', is_flag=True, help="Omit class Meta, created_at, updated_at, and __str__")
@click.argument("name")
@click.argument("attributes", nargs=-1, required=False)
@click.pass_context
def model(ctx, admin, abstract, no_defaults, name, attributes):
    """
    Generates a model under the models directory
    \f
    One can specify multiple attributes after the model's name, like so:
    \b
    User char:name date:birthday float:height email:email image:photo

    If the model is to be added to admin.site one can optionally opt in by specifying the --admin flag.
    """

    not_an_app_directory_warning(ctx)

    # Default model directory
    base_dir = 'models/'

    # Default helper
    helper = ModelHelper()

    # Parse args and create model
    content = helper.create(name=name, attributes=attributes, no_defaults=no_defaults, abstract=abstract)

    # TODO: handle --admin flag
    # TODO: handle --no_defaults flag

    # Handling --dry flag
    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        name = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=name, file_content=content)
            log_success(f"Created model {name}")
        except FileExistsError:
            log_error(f"File {name} already exists")
            return


@generate.command()
@click.option('--read-only', is_flag=True, help="For a read-only resource api endpoint")
@click.argument("name", required=True)
@click.pass_context
def viewset(ctx, read_only, name):
    """
    Generates a viewset for a serializable model
    \f
    Places the viewset under the viewset directory
    """

    not_an_app_directory_warning(ctx)

    # Default viewset directory
    base_dir = 'viewsets/'

    # Default helper
    helper = ViewSetHelper()

    # Parse template
    content = helper.create(name=name, read_only=read_only)

    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        name = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=name, file_content=content)
            log_success(f"Created viewset {name}")
        except FileExistsError:
            log_error(f"File {name} already exists")
            return


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def serializer(ctx, name):
    """
    Generates a serializer for a given model
    \f
    Checks for the existence of the specified model in models.py
    before attempting to create a serializer for it. Aborts if model is not found.
    """

    not_an_app_directory_warning(ctx)

    # Default serializer directory
    base_dir = 'serializers/'

    # ViewSet Helper
    helper = SerializerHelper()

    # Parse template
    content = helper.create(name=name)

    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        name = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=name, file_content=content)
            log_success(f"Created serializer {name}")
        except FileExistsError:
            log_error(f"File {name} already exists")
            return


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def form(ctx, name):
    """
    Generates a model form
    """

    not_an_app_directory_warning(ctx)

    # Default forms directory
    base_dir = 'forms/'

    # Form Helper
    helper = FormHelper()

    # Parse template
    content = helper.create(name=name)

    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        name = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=name, file_content=content)
            log_success(f"Created form {name}")
        except FileExistsError:
            log_error(f"File {name} already exists")
            return


@generate.command()
@click.argument("name", required=True)
@click.pass_context
def template(ctx, name):
    """
    Generates an html template
    """

    not_an_app_directory_warning(ctx)

    # Default forms directory
    base_dir = 'templates/'

    # Template Helper
    helper = TemplateHelper()

    # Parse template
    content = helper.create(name=name)

    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        name = f"{name.lower()}.html"

        try:
            helper.create_file(path=base_dir, filename=name, file_content=content)
            log_success(f"Created template {name}")
        except FileExistsError:
            log_error(f"File {name} already exists")
            return
