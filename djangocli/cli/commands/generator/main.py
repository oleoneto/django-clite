import click
import os
from djangocli.cli import log_error, log_success
from .helpers.model import ModelHelper
from .helpers.viewset import ViewSetHelper
from .helpers.serializer import SerializerHelper
from .helpers.form import FormHelper
from .helpers.template import TemplateHelper
from .helpers.admin import AdminHelper
from .helpers.view import ViewHelper

# Templates
from djangocli.cli.templates.viewset import ViewSetImportTemplate
from djangocli.cli.templates.model import modelImportTemplate


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
    ctx.obj['cwd'] = os.getcwd()


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
    base_dir = f"{ctx.obj['cwd']}/admin/"

    # Default helper
    helper = AdminHelper()
    filename = f"{name.lower()}.py"

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
        try:
            helper.create_file(path=base_dir, filename=filename, file_content=content)

            if inline:
                log_success(f"Created admin inline model {name.capitalize()} in {filename}")
                helper.add_admin_inline_import_to_init(path=base_dir, name=name)
                return
            log_success(f"Created admin model {name.capitalize()} in {filename}")
            helper.add_admin_import_to_init(path=base_dir, name=name)
        except FileExistsError:
            log_error(f"File {name} already exists")
            return


@generate.command()
@click.option('--register-admin', is_flag=True, help="Register model to admin site")
@click.option('--register-inline', is_flag=True, help="Register model to admin site as inline")
@click.option('--abstract', is_flag=True, help="Creates an abstract model type")
@click.argument("name")
@click.argument("attributes", nargs=-1, required=False)
@click.pass_context
def model(ctx, register_admin, register_inline, abstract, name, attributes):
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
    base_dir = f"{ctx.obj['cwd']}/models/"

    # Default helper
    helper = ModelHelper()

    # Parse args and create model
    content = helper.create(model=name, attributes=attributes, abstract=abstract)

    # Handling --dry flag
    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        filename = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=filename, file_content=content)

            if register_admin:
                ctx.invoke(admin, name=name)

            if register_inline:
                ctx.invoke(admin, name=name, inline=True)

            # Ensure model is imported in __init__
            helper.add_import(path=base_dir, template=modelImportTemplate, model=name)
            log_success(f"Created model {name.capitalize()} in {filename}")
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
    base_dir = f"{ctx.obj['cwd']}/viewsets/"

    # Default helper
    helper = ViewSetHelper()

    # Parse template
    content = helper.create(name=name, read_only=read_only)

    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        filename = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=filename, file_content=content)
            helper.add_import(path=base_dir, template=ViewSetImportTemplate, model=name)
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
    base_dir = f"{ctx.obj['cwd']}/serializers/"

    # ViewSet Helper
    helper = SerializerHelper()

    # Parse template
    content = helper.create(name=name)

    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        filename = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=filename, file_content=content)
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
    base_dir = f"{ctx.obj['cwd']}/forms/"

    # Form Helper
    helper = FormHelper()

    # Parse template
    content = helper.create(name=name)

    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        filename = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=filename, file_content=content)
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
    base_dir = f"{ctx.obj['cwd']}/templates/"

    # Template Helper
    helper = TemplateHelper()

    # Parse template
    content = helper.create(name=name)

    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        filename = f"{name.lower()}.html"

        try:
            helper.create_file(path=base_dir, filename=filename, file_content=content)
            log_success(f"Created template {filename}")
        except FileExistsError:
            log_error(f"File {filename} already exists")
            return


@generate.command()
@click.argument("name", required=True)
@click.option('--list', is_flag=True, help="Create model list view")
@click.option('--detail', is_flag=True, help="Create model list view")
@click.pass_context
def view(ctx, name, list, detail):
    """
    Generates a view
    """

    not_an_app_directory_warning(ctx)

    # Default forms directory
    base_dir = f"{ctx.obj['cwd']}/views/"

    # Template Helper
    helper = ViewHelper()

    # Parse template
    content = helper.create(name=name, list=list, detail=detail)

    if ctx.obj['dry']:
        log_success(content)
        return
    else:
        filename = f"{name.lower()}.py"

        try:
            helper.create_file(path=base_dir, filename=filename, file_content=content)
            log_success(f"Created view {name} in {filename}")
        except FileExistsError:
            log_error(f"File {filename} already exists")
            return


@generate.command()
@click.argument("name", required=True)
@click.argument("attributes", nargs=-1, required=False)
@click.pass_context
def resource(ctx, name, attributes):
    """
    Generates an API resource \f
    Full implementation includes model, serializer, viewset, and router endpoint
    """
    # TODO: Check undesired recursive behaviors
    # creates admin/admin/inline/model.py
    # may need to update BaseHelper
    ctx.invoke(model, name=name, register_admin=True, register_inline=True, attributes=attributes)
    ctx.invoke(serializer, name=name)
    ctx.invoke(viewset, name=name)
    ctx.invoke(form, name=name)
    ctx.invoke(template, name=name)
    ctx.invoke(view, name=name, list=True)
