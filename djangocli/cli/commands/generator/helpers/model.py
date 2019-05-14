import inflect
import json
import os
import fileinput
from djangocli.cli.commands.base_helper import BaseHelper
from djangocli.cli.templates.model import modelAttributeTemplate
from djangocli.cli.templates.model import modelTemplate

p = inflect.engine()
__DIR__ = os.path.dirname(os.path.abspath(__file__))
file = open(f'{__DIR__}/fields.json')
data = json.load(file)
file.close()

supported_fields = []
types = data['reserved_words']
relationships = data['reserved_words'][0]['relationships']


class ModelHelper(BaseHelper):

    # Store import statements
    extra_imports = []

    # Store attributes
    attributes_list = []

    def get_token_type(self, token):
        # Token char:name, float:price
        token = token.split(":")
        token_type = token[0].lower()
        token_name = token[1].lower()

        for i in token:
            if len(i) <= 1:
                return None

        # Checks if type is a relationship field
        for t in relationships:
            if token_type in t:
                return token_name, t.get(token_type)

        # Checks if type is a generic field
        for t in types:
            if token_type in t:
                return token_name, t.get(token_type)
        return None
    # end def

    def get_options(self, model_name, attribute_name, attribute_type):
        options = 'blank=True'

        if attribute_type == "BooleanField":
            options = "default=False"

        elif attribute_type == "CharField":
            options = "max_length=30"

        elif attribute_type == "ForeignKey":
            options = f"{attribute_name.capitalize()}, " \
                f"related_name='{p.plural(model_name.lower())}', " \
                f"on_delete=models.PROTECT"
            self.append_import(attribute_name)

        elif attribute_type == "ImageField" or attribute_type == "FileField":
            options += ", upload_to='uploads/'"

        elif attribute_type == "ManyToManyField":
            options = f"{attribute_name.capitalize()}, blank=True"
            self.append_import(attribute_name)

        elif attribute_type == "OneToOneField":
            options = f"{model_name.capitalize()}, " \
                f"related_name='{model_name.lower()}', " \
                f"on_delete=models.CASCADE"
            self.append_import(attribute_name)

        elif attribute_type == "SlugField":
            options = "unique=True"

        return options
    # end def

    def get_imports(self):
        return self.extra_imports
    # end def

    def get_app_name(self):
        # print(os.listdir('.'))
        for line in fileinput.input('apps.py'):
            if "name = " in line:
                fileinput.close()
                return line.split(" = ")[1].lstrip().replace("\n", "")
        fileinput.close()
        return "app"

    def append_import(self, value):
        if value not in self.extra_imports:
            self.extra_imports.append(value)
    # end def

    def parse_attributes(self, *args, **kwargs):
        # Parse and store each attribute
        if kwargs['attributes']:
            for attribute in kwargs['attributes']:

                try:
                    attribute_name = self.get_token_type(attribute)[0]
                    attribute_type = self.get_token_type(attribute)[1]

                    if attribute_type is not None:
                        options = self.get_options(model_name=kwargs['model'],
                                                   attribute_type=attribute_type,
                                                   attribute_name=attribute_name)
                        parsed_attribute = self.parse_template(name=attribute_name,
                                                               options=options,
                                                               type=attribute_type,
                                                               template=modelAttributeTemplate)

                        self.attributes_list.append(parsed_attribute)
                except TypeError:
                    pass

    # Interface method
    def create(self, *args, **kwargs):
        self.parse_attributes(**kwargs)
        app_name = self.get_app_name().replace("'", "")
        model_singular_name = kwargs['model']
        model_plural_name = p.plural(kwargs['model']).lower()
        db_table_name = f"{app_name}_{model_plural_name}"

        return self.parse_template(template=modelTemplate,
                                   imports=self.get_imports(),
                                   model=model_singular_name,
                                   db_table=db_table_name,
                                   attributes=self.attributes_list,
                                   abstract=kwargs['abstract'])
    # end def

    # Check model in scope
    def check_model_in_scope(self, model, scope):
        # Move to app scope
        # Look for model in models/{{ model.lower() }}.py
        pass
    # end def
