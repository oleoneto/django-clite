import click
import shutil
from commands.helpers.generator import *
from jinja2 import Template


@click.group()
@click.pass_context
def generate(ctx):
    """
    Model, route, and template generator
    """
    pass


@generate.command()
@click.option('--no-admin', is_flag=True, help="Do not add model to admin site")
@click.argument("name")
@click.argument("attributes", nargs=-1, required=False)
def model(no_admin, name, attributes):
    """
    Generates a model in models.py
    \f
    One can specify multiple attributes after the model's name, like so:
    \b
    User Char:name Date:birthday Float:height Email:email Image:photo

    Also adds model to admin.site by default. One can optionally opt out by specifying the --no-admin flag.
    """

    attribute_template = Template("{{name}} = models.{{type}}({{options}})")

    if attributes:
        for attr in attributes:

            attribute = type_for_token(attr)

            if attribute:
                options = default_options_for_attribute(attribute, name)
                at = attribute_template.render(name=attribute[0], type=attribute[1], options=options)
                click.secho(at, fg="green")


@generate.command()
@click.option('--no-template', is_flag=True, help="Do not generate a template file")
@click.option('--no-url', is_flag=True, help="Do not include in app's url patterns")
@click.argument("name")
def route(no_template, no_path, name):
    """
    Generates a route (or view)
    \f
    Command also attempts to create an html template file with the same name as the route. One can opt out
    of this behavior by specifying the --no-template flag.
    Unless --no-url is set, the command also adds the route to urls.py

    """
    pass


@generate.command()
@click.argument("name")
def viewset(name):
    """
    Generates a viewset for a serializable model
    \f
    Checks for the existence of the serializable model in serializers.py
    before attempting to create a viewset for it. Aborts if serializer is not found.
    """
    # shutil.copytree('blueprints', 'leo')
    pass


@generate.command()
@click.option('--add-model', is_flag=True, help="Adds the model to models.py if it does not exist")
@click.argument("name")
def serializer(add_model, name):
    """
    Generates a serializer for a given model
    \f
    Checks for the existence of the specified model in models.py
    before attempting to create a serializer for it. Aborts if model is not found.
    """
    pass


