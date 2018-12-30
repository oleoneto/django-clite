
import os
import json
from commands.helpers.templater import *


file = open('config/config.json')
data = json.load(file)
file.close()

supported_fields = []
supported_frameworks = []
types = data['reserved_words']
relationships = data['reserved_words'][0]['relationships']
frameworks = data['supported_frameworks']

for i in frameworks[0].keys():
    supported_frameworks.append(i)


def type_for_token(token):

    token = token.split(":")
    token[0] = token[0].capitalize()
    token[1] = token[1].lower()

    for i in token:
        if not len(i) > 1:
            return None

    # Checks if type is a relationship field
    for _type_ in relationships:
        if token[0] in _type_:
            return token[1], _type_.get(token[0])

    # Checks if type is a generic field
    for _type_ in types:
        if token[0] in _type_:
            return token[1], _type_.get(token[0])
    return None


def default_options_for_attribute(attr, model):

    _name_ = attr[0]
    _type_ = attr[1]

    options = 'blank=True'

    if _type_ == "CharField":
        options += ", max_length=30"
    elif _type_ == "BooleanField":
        options = "default=False"
    elif _type_ == "SlugField":
        options = "unique=True"
    elif _type_ == "ImageField" or _type_ == "FileField":
        options += ", upload_to='/uploads/'"
    elif _type_ == "ForeignKey":
        related_name = p.plural(model.lower())
        options = "{}, {}, {}".format(_name_.capitalize(), "related_name='{}'".format(related_name), "on_delete=models.DO_NOTHING")
    elif _type_ == "OneToOneField":
        related_name = model.lower()
        options = "{}, {}, {}".format(_name_.capitalize(), "related_name='{}'".format(related_name), "on_delete=models.CASCADE")
    elif _type_ == "ManyToManyField":
        options = "{}".format(_name_.capitalize())
    return options


def links_for_framework(framework):
    framework = framework.lower()

    css = frameworks[0][framework]['css']
    js = frameworks[0][framework]['js']

    return css, js


def create_file(filename, content):
    _dir_ = os.getcwd()
    os.chdir("tests/outputs")

    f = None

    try:
        f = open(filename, 'r')
        if f:
            raise FileExistsError
    except FileNotFoundError:
        with open(filename, 'w') as f:
            f.write(content)
            f.write('\n')
        f.close()
        os.chdir(_dir_)


def append_to_file(filename, content):
    _dir_ = os.getcwd()
    os.chdir("tests/outputs")

    with open(filename, 'a') as f:
        f.write("\n")
        f.write(content)
        f.write("\n")
    f.close()
    os.chdir(_dir_)


def replace_contents_of_file(in_filename, lookup, replacement, out_filename):
    with open(in_filename, 'r') as in_file:
        file_data = in_file.read()
        file_data = file_data.replace(lookup, replacement)

    with open(out_filename, 'w') as out_file:
        out_file.write(file_data)


def framework_handler(framework):
    __f__ = links_for_framework(framework)
    if __f__:
        framework = __f__
        _html_ = html_template.render(route=route, framework=framework)
    else:
        _html_ = html__simple_template.render(route=route, framework=framework)


def create_route(route, framework):
    # TODO: Implement create_route
    # Render html parent template
    _route = "A"
    if framework:
        framework_handler(framework)
    return _route


def create_subroute(route, parent):
    # TODO: Implement create_subroute
    # Render html child template
    _route = "A"
    return _route


def routes_generator_handler(route, framework):
    # TODO: Implement routes_generator_handler with template extensions

    routes = route.split('/')
    generated_routes = []
    parent = None

    if len(routes) == 1:
        generated_routes.append(create_route(route, framework=framework))
        return

    for n in range(len(routes)):
        if n == 0:
            parent = create_route(routes[0], framework=framework)
            generated_routes.append(parent)

        r = create_subroute(routes[n], parent=parent)
        generated_routes.append(r)

        # Make routes[0] a parent
        # Create html for each child template
        # Make routes[1+] extend parent
        # Add framework to parent only
        pass

    return generated_routes
