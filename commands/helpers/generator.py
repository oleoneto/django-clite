import shutil
import os
import json
from pprint import pprint
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

    for _type_ in relationships:
        if token[0] in _type_:
            return token[1], _type_.get(token[0])

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
    elif _type_ == "ImageField" or _type_ == "FileField":
        options += ", upload_to=/uploads/"
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

    with open(filename, 'w') as f:
        f.write(content)
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
