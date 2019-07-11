import click
import fileinput
import inflection
import json
import os
from djangle.cli import log_success, sanitized_string
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.model import (
    auth_user_model_template,
    model_field_template,
    model_import_template,
    model_template,
)


DEFAULT_NOT_IN_SCOPE_WARNING = """Cannot find model {} in {} scope. Want to create model?"""


class ModelHelper(BaseHelper):

    imports_list = []

    fields_list = []

    @classmethod
    def append_import(cls, value):
        if value not in cls.imports_list:
            cls.imports_list.append(value)

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        app_name = self.get_app_name()

        path = kwargs['path']

        filename = f"{model}.py"

        db_table_name = f"{app_name}_{inflection.pluralize(model)}"

        self.parse_fields(**kwargs)

        self.parse_and_create(
            model=model,
            abstract=kwargs['abstract'],
            fields=self.fields_list,
            imports=self.imports_list,
            db_table=db_table_name,
            template=model_template,
            filename=filename,
            path=path,
            dry=kwargs['dry']
        )

        self.add_import(**kwargs, template=model_import_template)

        log_success("Successfully created model.")

    @classmethod
    def create_auth_user(cls, **kwargs):

        kwargs['model'] = 'User'

        kwargs['filename'] = 'user.py'

        kwargs['path'] = f"{kwargs['path']}/models/"

        cls.parse_and_create(
            model=kwargs['model'],
            filename=kwargs['filename'],
            project_name=kwargs['project'],
            template=auth_user_model_template,
            path=kwargs['path']
        )

        cls.add_import(**kwargs, template=model_import_template)

        log_success("Successfully created model.")

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        filename = f"{model.lower()}.py"

        template = model_import_template

        if self.destroy(filename=filename, **kwargs):

            self.remove_import(template=template, **kwargs)

            log_success('Successfully deleted model.')

    @classmethod
    def find_resource_in_scope(cls, model):
        """
        Searches the current directory for the specified model
        either by filename or import statement in __init__.py

        If the model is not found in the current scope, a warning is displayed
        indicating that user input is needed to proceed with the command.
        """
        path = f"{os.getcwd()}/models"

        init = f"{path}/__init__.py"

        app_name = cls.get_app_name()

        filename = model.lower()

        if not model.endswith('.py'):
            filename += '.py'

        if filename in os.listdir(path):
            return

        for line in fileinput.input(init):
            if model.capitalize() in line:
                fileinput.close()
                return
        fileinput.close()

        if click.confirm(DEFAULT_NOT_IN_SCOPE_WARNING.format(model.capitalize(), app_name)):
            # TODO: Create model in question...
            pass

    @classmethod
    def get_app_name(cls):
        """
        Searches current directory for apps.py in order to
        retrieve the application name from it.
        """
        try:
            for line in fileinput.input('apps.py'):
                if "name = " in line:
                    fileinput.close()
                    return line.split(" = ")[1].lstrip().replace("\n", "").replace("'", "")
            fileinput.close()
        except FileNotFoundError:
            return "app"
        return "app"

    @classmethod
    def handle_tokens(cls, field):
        """
        Should parse input attribute into individual tokens.
        Expect input to be of the form (char:name, text:bio, image:artwork)
        """

        # TODO: Fix implementation to prevent issue-69
        filepath = f'{os.path.dirname(os.path.abspath(__file__))}/fields.json'

        file = open(filepath)

        data = json.load(file)

        file.close()

        default_token_types = data['reserved_words']

        relationships = default_token_types[0]['relationships']

        # i.e char:first_name
        parsed_token = field.split(":")

        # i.e char
        parsed_token_type = parsed_token[0]

        # i.e first_name
        parsed_token_name = parsed_token[1]

        # Ensure token exists and has minimum required length of 2
        for part in parsed_token:
            if len(part) < 2:
                return None

        # Check if parsed_token_type is a relationship field
        for relationship in relationships:
            if parsed_token_type in relationship:
                return sanitized_string(parsed_token_name), relationship.get(parsed_token_type)

        # Check if parsed_token_type is a generic model field
        for some in default_token_types:
            if parsed_token_type in some:
                return sanitized_string(parsed_token_name), some.get(parsed_token_type)

        return None

    @classmethod
    def handle_field(cls, model, field_name, field_type):
        """
        Determines what options are present with each model field.
        """

        default_model_options = (
            ('BooleanField', 'default=False'),
            ('CharField', 'max_length=50'),
            ('DateField', 'auto_now=True'),
            ('DateTimeField', 'auto_now=True'),
            ('FileField', "blank=True, upload_to='uploads/files/'"),
            ('ForeignKey', "{}, related_name='{}', on_delete=models.PROTECT"),
            ('ImageField', "blank=True, upload_to='uploads/images/'"),
            ('ManyToManyField', '{}, blank=True'),
            ('OneToOneField', "{}, related_name='{}', on_delete=models.CASCADE"),
            ('SlugField', 'unique=True'),
            ('TextField', 'blank=True'),  # <-- Added to address issue-69
            ('TimeField', 'auto_now=True'),
        )

        # TODO: Fix implementation to prevent issue-69
        for field, options in default_model_options:
            if field.lower() == field_type.lower():
                if field == "ForeignKey":
                    options = options.format(
                        field_name.capitalize(),
                        inflection.pluralize(model).lower()
                    )
                    cls.find_resource_in_scope(field_name)
                    cls.append_import(field_name)

                elif field == "ManyToManyField":
                    options = options.format(
                        field_name.capitalize()
                    )
                    cls.find_resource_in_scope(field_name)
                    cls.append_import(field_name)

                elif field == "OneToOneField":
                    options = options.format(
                        field_name.capitalize(),
                        inflection.singularize(model)
                    )
                    cls.find_resource_in_scope(field_name)
                    cls.append_import(field_name)

                return model_field_template.render(
                    name=field_name,
                    type=field,
                    options=options
                )

    @classmethod
    def parse_fields(cls, **kwargs):
        """
        Parses and saves field data in fields_list for future reference
        """
        try:
            fields = kwargs['fields']
        except KeyError:
            return

        for field in fields:
            try:
                f_name, f_type = cls.handle_tokens(field)

                if f_type is not None and f_name is not None:
                    field_content = cls.handle_field(
                        field_type=f_type,
                        field_name=f_name,
                        model=kwargs['model']
                    )

                    cls.fields_list.append(field_content)

            except TypeError:
                return
