import click
import shutil
from commands.helpers.generator import *
from commands.helpers.echoer import successful, error, file_created, file_exists


@click.group()
@click.pass_context
@click.option('--dry', is_flag=True, help="Display output without creating files")
@click.option('--save', is_flag=True, help="Saves all output to a file")
def generate(ctx, dry, save):
    """
    Model, route, and template generator
    """
    ctx.ensure_object(dict)
    ctx.obj['dry'] = dry
    ctx.obj['save'] = save


@generate.command()
@click.option('--admin', is_flag=True, help="Register model to admin site")
@click.option('--abstract', is_flag=True, help="Creates an abstract model type")
@click.option('--no-defaults', is_flag=True, help="Omit class Meta, created_at, updated_at, and __str__")
@click.argument("name")
@click.argument("attributes", nargs=-1, required=False)
@click.pass_context
def model(ctx, admin, abstract, no_defaults, name, attributes):
    """
    Generates a model in models.py
    \f
    One can specify multiple attributes after the model's name, like so:
    \b
    User Char:name Date:birthday Float:height Email:email Image:photo

    `created_at` and `updated_at` are added to a model by default unless --no-defaults is specified.

    If the model is to be added to admin.site one can optionally opt in by specifying the --admin flag.
    """

    # Attributes of the form field:name ...
    _attributes_ = []

    # The attribute to be used as the return of __str__
    _descriptor_ = None

    # Splitting the field and attribute names from the field:name input
    if attributes:
        for attr in attributes:

            attribute = type_for_token(attr)

            # Decides which of the attributes is to be used in as the return of __str__
            if attribute:
                if attribute[1] == "CharField":
                    _descriptor_ = attribute[0]
                options = default_options_for_attribute(attribute, name)
                at = attribute_template.render(name=attribute[0], type=attribute[1], options=options)
                _attributes_.append(at)

    # --no-defaults creates a simpler model
    if no_defaults:
        _model_ = model_simple_template.render(model=name, attributes=_attributes_)
    else:
        _model_ = model_template.render(model=name, abstract=abstract, attributes=_attributes_, descriptor=_descriptor_)

    # --dry and --save flags
    if ctx.obj['dry']:
        # Console log the model
        successful(_model_)
        return
    elif ctx.obj['save']:
        try:
            name = "%s_model.py" % name
            create_file(name, _model_)
            file_created(name)
        except FileExistsError:
            file_exists()
        return

    # TODO: Handle file output for models.py
    file_created(name)


@generate.command()
@click.pass_context
@click.option('--no-template', is_flag=True, help="Do not generate a template file")
@click.option('--no-url', is_flag=True, help="Do not include in app's url patterns")
@click.option('--framework', help="Name of css framework to link in stylesheets", type=click.Choice(supported_frameworks))
@click.argument("name", required=True)
def route(ctx, no_template, no_url, framework, name):
    """
    Generates a route (or view)
    \f
    Command also attempts to create an html template file with the same route as the route. One can opt out
    of this behavior by specifying the --no-template flag.
    Unless --no-url is set, the command also adds the route to urls.py

    """
    name = name.lower()

    # TODO: Implement handler for route/subroute
    routes_generator_handler(name, framework=framework)

    # --frameworks flag for default frameworks
    # Checks if framework is supported and gets the appropriate css and js links
    # Adds framework.css and framework.js to template if framework is not supported
    if framework:
        _f = links_for_framework(framework)
        if _f:
            framework = _f
            _html_ = html_template.render(route=name, framework=framework)
        else:
            _html_ = html__simple_template.render(route=name, framework=framework)
    else:
        _html_ = html__simple_template.render(route=name)

    # Defines the view method for the route
    _route_ = route_template.render(route=name)

    # Defines the url pattern for the route
    # A route named 'index' will be added as '/' and not by route
    _route_url_ = route_url_template.render(route=name)

    # --dry and --save flags
    # --dry simply logs to console
    # --save attempts to create file if none exist in default output directory
    if ctx.obj['dry']:
        successful(_route_)
        successful(_route_url_)
        successful(_html_)
        return
    elif ctx.obj['save']:
        try:
            route_file = "%s_route.py" % name
            create_file(route_file, _route_)
            file_created(route_file)

            html_file = "%s_template.html" % name
            create_file(html_file, _html_)
            file_created(html_file)
        except FileExistsError:
            error('File already exists')
        return

    # TODO: test create_file_(filename, content)
    append_to_file("view.py", _route_)

    replace_contents_of_file('urls.dc', ']', _route_url_, 'urls.py')

    # TODO: test create_file_(filename, content)
    create_file("{}.html".format(name), _html_)


@generate.command()
@click.option('--read-only', is_flag=True, help="Support only support GET requests")
@click.argument("name", required=True)
def viewset(read_only, name):
    """
    Generates a viewset for a serializable model
    \f
    Checks for the existence of the serializable model in serializers.py
    before attempting to create a viewset for it. Aborts if serializer is not found.
    """

    name = name.capitalize()

    _viewset_ = viewset_template.render(model=name, read_only=read_only)

    # TODO: Add file output
    successful("Output to viewsets.py")
    successful(_viewset_)


@generate.command()
@click.argument("name", required=True)
def serializer(name):
    """
    Generates a serializer for a given model
    \f
    Checks for the existence of the specified model in models.py
    before attempting to create a serializer for it. Aborts if model is not found.
    """

    # TODO: Add file output
    _serializer_ = serializer_template.render(model=name)
    click.secho("Output to serializers.py", fg='green')
    click.secho(_serializer_, fg="green")


@generate.command()
@click.argument("name", required=True)
def form(name):
    """
    Generates a model form
    """

    _form_ = form_template.render(model=name)

    # TODO: Add file output
    click.secho("Output to forms.py", fg='green')
    click.secho(_form_, fg="green")
