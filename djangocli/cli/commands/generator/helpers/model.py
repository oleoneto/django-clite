from .base import *
import json
import inflect
from djangocli.cli.templates.model import model_attribute
from djangocli.cli.templates.model import model as mt_
from djangocli.cli.templates.model import model_simple

p = inflect.engine()

file = open('djangocli/config.json')
data = json.load(file)
file.close()

supported_fields = []
supported_frameworks = []
types = data['reserved_words']
relationships = data['reserved_words'][0]['relationships']
frameworks = data['supported_frameworks']

for i in frameworks[0].keys():
    supported_frameworks.append(i)


class ModelHelper(BaseHelper):

    def parse_options(self, attr, current_model):
        attribute_name = attr[0]
        attribute_type = attr[1]

        options = 'blank=True'
        imports = None

        if attribute_type == "CharField":
            options += ", max_length=30"
        elif attribute_type == "BooleanField":
            options = "default=False"
        elif attribute_type == "SlugField":
            options = "unique=True"
        elif attribute_type == "ImageField" or attribute_type == "FileField":
            options += ", upload_to='uploads'"
        elif attribute_type == "ForeignKey":
            related_name = p.plural(current_model.lower())
            options = f"{attribute_name.capitalize()}, related_name='{related_name}', on_delete=models.DO_NOTHING"
            imports = attribute_name
        elif attribute_type == "OneToOneField":
            related_name = current_model.lower()
            options = f"{current_model.capitalize()}, related_name='{related_name}', on_delete=models.CASCADE"
            imports = attribute_name
        elif attribute_type == "ManyToManyField":
            options = f"{attribute_name.capitalize()}"
            imports = attribute_name
        return options, imports
    # end def

    def type_for(self, token):
        token = token.split(":")
        token[0] = token[0].capitalize()
        token[1] = token[1].lower()

        for i in token:
            if not len(i) > 1:
                return None

        # Checks if type is a relationship field
        for t in relationships:
            if token[0] in t:
                return token[1], t.get(token[0])

        # Checks if type is a generic field
        for t in types:
            if token[0] in t:
                return token[1], t.get(token[0])
        return None
    # end def

    def create(self, name, attributes, no_defaults, abstract):
        # Attributes in the form field:name
        ATTRIBUTES = []

        # Descriptor will be used with the __str__ method of the model
        DESCRIPTOR = None

        # Imports
        imports = []

        if attributes:
            for attr in attributes:
                attribute = self.type_for(attr)

                if attribute:
                    if attribute[1] == "CharField":
                        DESCRIPTOR = attribute[0]
                    options = self.parse_options(attribute, name)
                    imports.append(options[1])
                    attribute = model_attribute.render(name=attribute[0], type=attribute[1], options=options[0])
                    ATTRIBUTES.append(attribute)

        if no_defaults:
            return self.parsed_simple_model_template(name, ATTRIBUTES, imports)
        else:
            return self.parsed_model_template(name, ATTRIBUTES, imports, DESCRIPTOR, abstract)
    # end def

    def parsed_model_template(self, resource_name, attributes, imports, descriptor, abstract=False):
        return mt_.render(model=resource_name, abstract=abstract, attributes=attributes, imports=imports, descriptor=descriptor)
    # end def

    def parsed_simple_model_template(self, resource_name, attributes, imports):
        return model_simple.render(model=resource_name, attributes=attributes, imports=imports)
    # end def
