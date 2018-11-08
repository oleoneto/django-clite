import json
import jinja2
import inflect
from enum import Enum, unique

p = inflect.engine()

file = open('config/config.json')
data = json.load(file)
file.close()
types = data['reserved_words']
relationships = types[0]['relationships']


@unique
class ModelType(Enum):
    FK = "ForeignKey"
    One = "OneToOneField"


def type_for_token(token):

    token = token.split(":")

    for i in token:
        if not len(i) > 1:
            return None

    for type in relationships:
        if token[0] in type:
            return token[1], type.get(token[0])

    for type in types:
        if token[0] in type:
            return token[1], type.get(token[0])
    return None


def tokenized(arg):
    return arg.split(":")


def contains_key(key, _list):
    def contains(_list):
        return key in _list.values()
    return contains(_list)


def default_options_for_attribute(attr, model):

    name = attr[0]
    type = attr[1]

    options = 'blank=True'

    if type == "CharField":
        options += ", max_length=30"
    elif type == "ImageField" or type == "FileField":
        options += ", upload_to=/uploads/"
    elif type == "ForeignKey":
        related_name = p.plural(model.lower())
        options = "{}, {}, {}".format(name.capitalize(), "related_name='{}'".format(related_name), "on_delete=models.DO_NOTHING")
    elif type == "OneToOneField":
        related_name = model.lower()
        options = "{}, {}, {}".format(name.capitalize(), "related_name='{}'".format(related_name), "on_delete=models.CASCADE")
    elif type == "ManyToManyField":
        options = "{}".format(name.capitalize())
    return options
