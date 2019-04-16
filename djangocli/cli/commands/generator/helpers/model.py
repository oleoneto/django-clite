import inflect
import json
import os
from djangocli.cli.commands.base_helper import BaseHelper
from djangocli.cli.templates.model import model_attribute
from djangocli.cli.templates.model import model as mt_
from djangocli.cli.templates.model import model_simple

p = inflect.engine()
__DIR__ = os.path.dirname(os.path.abspath(__file__))
file = open(f'{__DIR__}/fields.json')
data = json.load(file)
file.close()

supported_fields = []
types = data['reserved_words']
relationships = data['reserved_words'][0]['relationships']


class ModelHelper(BaseHelper):

    def create(self, *args, **kwargs):
        # Attributes in the form field:name
        ATTRIBUTES = []

        # Imports
        imports = []

        if kwargs['attributes']:
            for attr in kwargs['attributes']:
                attribute = self.type_for(attr)

                if attribute:
                    options = self.parse_options(attribute, kwargs['name'])
                    imports.append(options[1])
                    attribute = model_attribute.render(name=attribute[0],
                                                       type=attribute[1],
                                                       options=options[0])
                    ATTRIBUTES.append(attribute)

        if kwargs['no_defaults']:
            return self.parsed_simple_model_template(model=kwargs['name'], attributes=ATTRIBUTES, imports=imports)
        else:
            return self.parsed_model_template(model=kwargs['name'], attributes=ATTRIBUTES, imports=imports, abstract=kwargs['abstract'])
    # end def

    def parse_options(self, attr, current_model):
        attribute_name = attr[0]
        attribute_type = attr[1]

        options = 'blank=True'
        imports = None
        special = False

        if attribute_name == "id":
            options = "primary_key=True, editable=False"
        elif attribute_type == "CharField":
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

    def parsed_model_template(self, *args, **kwargs):
        return mt_.render(**kwargs)
    # end def

    def parsed_simple_model_template(self, *args, **kwargs):
        return model_simple.render(**kwargs)
    # end def
