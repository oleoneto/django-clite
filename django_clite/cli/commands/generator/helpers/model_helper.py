import click
import fileinput
import inflection
import os
from django_clite.cli import log_success, sanitized_string, log_info
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.model import (
    auth_user_model_template,
    model_field_template,
    model_import_template,
    model_template,
)


DEFAULT_NOT_IN_SCOPE_WARNING = """Cannot find model {} in {} scope. Want to create model?"""

# Abbreviation, field name, default value
DEFAULT_MODEL_FIELDS = {
    'belongsto': "ForeignKey",
    'big': 'BigIntegerField',
    'bigint': 'BigIntegerField',
    'bool': 'BooleanField',
    'boolean': 'BooleanField',
    'char': 'CharField',
    'date': 'DateField',
    'datetime': 'DateTimeField',
    'dec': 'DecimalField',
    'decimal': 'DecimalField',
    'duration': 'DurationField',
    'email': 'EmailField',
    'file': "FileField",
    'filepath': 'FilePathField',
    'fk': "ForeignKey",
    'foreignkey': "ForeignKey",
    'float': 'FloatField',
    'hasone': "OneToOneField",
    'hasmany': 'ManyToManyField',
    'image': "ImageField",
    'int': 'IntegerField',
    'integer': 'IntegerField',
    'ipaddress': 'GenericIPAddressField',
    'many': 'ManyToManyField',
    'manytomany': 'ManyToManyField',
    'one': "OneToOneField",
    'onetoone': "OneToOneField",
    'photo': "ImageField",
    'slug': 'SlugField',
    'string': 'TextField',
    'text': 'TextField',
    'time': 'TimeField',
    'url': 'URLField',
    'uuid': 'UUIDField',
}

# Abbreviation, field name, default value
DEFAULT_MODEL_OPTIONS = {
    'BigIntegerField': '',
    'BooleanField': 'default=False',
    'CharField': 'max_length=100',
    'DateField': 'auto_now=True',
    'DateTimeField': 'auto_now=True',
    'DecimalField': '',
    'DurationField': '',
    'EmailField': '',
    'GenericIPAddressField': '',
    'FileField': "blank=True, upload_to='uploads/{}/'",
    'FilePathField': '',
    'FloatField': '',
    'ForeignKey': "{}, related_name='{}', on_delete=models.PROTECT",
    'ImageField': "blank=True, upload_to='uploads/{}/'",
    'IntegerField': '',
    'ManyToManyField': '{}, blank=True',
    'OneToOneField': "{}, related_name='{}', on_delete=models.CASCADE",
    'SlugField': 'unique=True',
    'TextField': 'blank=True',
    'TimeField': 'auto_now=True',
    'URLlField': '',
    'UUIDField': 'default=uuid.uuid4, editable=False',
}

DEFAULT_SPECIAL_INHERITABLE_TYPES = {
    'abstract-user': 'django.contrib.auth.models',
    'abstract-base-user': 'django.contrib.auth.models',
    'base-user': 'django.contrib.auth.models',
    'user': 'django.contrib.auth.models',
}


class ModelHelper(BaseHelper):

    # List of fields to be rendered in model template
    fields_list = []

    # List models referred to in ForeignKey, OneToOne, or ManyToMany fields.
    dependencies_list = []

    # List of imports to be rendered in model template
    imports_list = []

    # List of special imports to be rendered in model template
    special_import = []

    @classmethod
    def append_import(cls, value):
        if value not in cls.imports_list:
            cls.imports_list.append(value)

    @classmethod
    def append_special_import(cls, value):
        if value in DEFAULT_SPECIAL_INHERITABLE_TYPES:
            statement = DEFAULT_SPECIAL_INHERITABLE_TYPES[value]
            value = inflection.camelize(inflection.underscore(value))
            cls.special_import = (statement, value)
            return True
        else:
            model = inflection.camelize(inflection.underscore(value))
            value = inflection.underscore(value)
            cls.special_import = (f'.{value}', model)
        return False

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        base_model = self.check_noun(kwargs['inherits']) if kwargs['inherits'] else None

        # Check if model is in the `special` category before
        # attempting to create a module for it if one is not found.
        if base_model is not None:
            if not self.append_special_import(base_model):
                self.find_resource_in_scope(base_model)

        app_name = self.get_app_name()

        path = kwargs['path']

        filename = f"{model}.py"

        db_table_name = f"{app_name}_{inflection.pluralize(model)}"

        if kwargs['fields'] is not None:
            self.parse_fields(**kwargs)

        self.parse_and_create(
            model=model,
            abstract=kwargs['abstract'],
            base=self.special_import,
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

        # Ensure related models are created
        self.handle_dependencies(**kwargs, app_name=app_name)

        return

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
        asking the user whether the model should be created.
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
            cls.dependencies_list.append(model.capitalize())

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

    def handle_dependencies(self, **kwargs):

        if len(self.dependencies_list) < 1:
            return False

        for model in self.dependencies_list:
            app_name = kwargs['app_name']

            filename = f'{model.lower()}.py'

            db_table_name = f"{app_name}_{inflection.pluralize(model)}"

            self.parse_and_create(
                model=model,
                abstract=False,
                fields=[],
                imports=[],
                db_table=db_table_name,
                template=model_template,
                filename=filename,
                path=kwargs['path'],
                dry=kwargs['dry']
            )

            self.add_import(
                template=model_import_template,
                model=model,
                path=kwargs['path'],
                dry=kwargs['dry']
            )

        return True

    @classmethod
    def handle_tokens(cls, field):
        """
        Should parse input attribute into individual tokens.
        Expect input to be of the form (char:name, text:bio, image:artwork)
        """

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
        for abbreviation, field in DEFAULT_MODEL_FIELDS.items():
            if parsed_token_type.lower() == abbreviation.lower():
                return sanitized_string(parsed_token_name), DEFAULT_MODEL_FIELDS[abbreviation]

        return None

    @classmethod
    def handle_field(cls, model, field_name, field_type):
        """
        Determines what options are present with each model field.
        """

        if DEFAULT_MODEL_OPTIONS[field_type] is not None:
            if field_type == "ForeignKey":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(
                    field_name.capitalize(),
                    inflection.pluralize(model.lower())
                )
                cls.find_resource_in_scope(field_name)
                cls.append_import(field_name)

            elif field_type == "OneToOneField":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(
                      field_name.capitalize(),
                      inflection.singularize(model)
                  )
                cls.find_resource_in_scope(field_name)
                cls.append_import(field_name)

            elif field_type == "ManyToManyField":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(
                        field_name.capitalize()
                )
                cls.find_resource_in_scope(field_name)
                cls.append_import(field_name)

            elif field_type == "FileField" or "ImageField":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(inflection.pluralize(field_name))

            else:
                options = DEFAULT_MODEL_OPTIONS[field_type]

            return model_field_template.render(
                name=field_name,
                type=field_type,
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
                field_name, field_type = cls.handle_tokens(field)

                if field_type is not None and field_name is not None:
                    field_content = cls.handle_field(
                        field_type=field_type,
                        field_name=field_name,
                        model=kwargs['model']
                    )

                    cls.fields_list.append(field_content)

            except TypeError:
                return
