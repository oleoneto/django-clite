import os
import click
import inflection
import fileinput
from jinja2 import Template
from .logger import log_error
from .fs import FSHelper
from .parser import sanitized_string
from .templates import rendered_file_template
from faker import Faker
from faker.providers import company, date_time, internet, misc

fake = Faker()
fake.add_provider(company)
fake.add_provider(date_time)
fake.add_provider(internet)
fake.add_provider(misc)

DEFAULT_NOT_IN_SCOPE_WARNING = """Cannot find model {} in {} scope. Want to create model?"""

# Abbreviation, Django field type
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
    'ip': 'GenericIPAddressField',
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

# Django field type, default value
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
    'URLField': '',
    'UUIDField': 'default=uuid.uuid4, editable=False',
}

JSON_COMPATIBLE_FIELDS = {
    'BigIntegerField': 'pyint',
    'BooleanField': 'pybool',
    'CharField': 'text',
    'DateField': 'future_date',
    'DateTimeField': 'iso8601',
    'DecimalField': 'pydecimal',
    'EmailField': 'safe_email',
    'GenericIPAddressField': 'ipv4',
    'FileField': 'file_path',
    'FilePathField': 'file_path',
    'FloatField': 'pyfloat',
    'ImageField': 'image_url',
    'IntegerField': 'pyint',
    'SlugField': 'slug',
    'TextField': 'text',
    'TimeField': 'time',
    'URLField': 'url',
    'UUIDField': 'uuid4',
}

DEFAULT_SPECIAL_INHERITABLE_TYPES = {
    'abstract-user': 'django.contrib.auth.models',
    'abstract-base-user': 'django.contrib.auth.models',
    'base-user': 'django.contrib.auth.models',
    'user': 'django.contrib.auth.models',
}

UNSUPPORTED_ADMIN_FIELD_TYPES = {
    'FileField',
    'FilePathField',
    'ImageField',
    'ManyToManyField',
    'TextField'
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'commands/generator/templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class FieldParser(FSHelper):
    # Field names and types
    fixture_fields = []

    # List of fields to be rendered in model template
    fields_list = []

    # List models referred to in ForeignKey, OneToOne, or ManyToMany fields.
    dependencies_list = []

    # List of imports to be rendered in model template
    imports_list = []

    # List of special imports to be rendered in model template
    special_import = []

    # List of fields for admin model
    admin_fields_list = []

    ####################################

    def __handle_tokens(self, field):
        """
        Should parse input attribute into individual tokens.
        Expect input to be of the form (char:name, text:bio, image:artwork)

        :param field: model field to be parsed
        :return: (field name, Django field type) or None
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

    def __handle_fixture(self, field_name, field_type):
        if field_type in JSON_COMPATIBLE_FIELDS:
            fixture_template = Template('''"{{ field_name }}": {{ field_value }},''')
            value = getattr(fake, JSON_COMPATIBLE_FIELDS[field_type])()

            if type(value).__name__ == 'str':
                value = f'"{value}"'

            if type(value).__name__ == 'bool':
                value = f'{value}'.lower()

            content = fixture_template.render(
                field_name=field_name,
                field_value=value
            )
            self.__append_fixture_field(content)

    def __handle_field(self, model, field_name, field_type):
        """
        Determines what options are present with each model field.

        :param model: the current model
        :param field_name: name of model field. i.e. first_name
        :param field_type: type of model field. i.e. CharField
        :return:
        """

        # Parse field type and name for fixtures
        self.__handle_fixture(field_name, field_type)

        # Parse field type and name for model
        if DEFAULT_MODEL_OPTIONS[field_type] is not None:
            template = 'model-field.tpl'

            if field_type == "ForeignKey":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(
                    field_name.capitalize(),
                    inflection.pluralize(model.lower())
                )
                self.find_resource_in_scope(field_name)
                self.append_import(field_name)

            elif field_type == "OneToOneField":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(
                    field_name.capitalize(),
                    inflection.singularize(model)
                )
                self.find_resource_in_scope(field_name)
                self.append_import(field_name)

            elif field_type == "ManyToManyField":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(
                    field_name.capitalize()
                )
                self.find_resource_in_scope(field_name)
                self.append_import(field_name)

            elif field_type == "FileField" or "ImageField":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(inflection.pluralize(field_name))

            else:
                options = DEFAULT_MODEL_OPTIONS[field_type]

                # Save model for admin list
                log_error(field_name)
                log_error(field_type)

            if field_type not in UNSUPPORTED_ADMIN_FIELD_TYPES:
                self.__append_admin_field(field_name)

            return rendered_file_template(
                path=TEMPLATE_DIR,
                template=template,
                context={
                    'name': field_name,
                    'type': field_type,
                    'options': options,
                    'lazy_name': field_name.replace("_", " "),
                }
            )

    def __append_admin_field(self, value):
        # TODO: Add default `id` field
        if value not in self.admin_fields_list:
            self.admin_fields_list.append(value)

    def __append_fixture_field(self, value):
        """Ensure last key does not have an added comma"""
        if value not in self.fixture_fields:
            if len(self.fixture_fields) > 0:
                self.fixture_fields[-1] += ','
            value = value.replace(',', '')
            self.fixture_fields.append(value)

    def parse_fields(self, model, fields):
        """
        Parses and saves field data in fields_list for future reference

        :param model: the name of the current model
        :param fields: the model fields to be parsed
        :param kwargs:
        :return:
        """

        for field in fields:
            try:
                field_name, field_type = self.__handle_tokens(field)

                if field_type is not None and field_name is not None:
                    field_content = self.__handle_field(
                        field_type=field_type,
                        field_name=field_name,
                        model=model
                    )

                    self.fields_list.append(field_content)

            except TypeError:
                return

    def find_resource_in_scope(self, model):
        """
        Searches the current directory for the specified model
        either by filename or import statement in __init__.py

        If the model is not found in the current scope, a warning is displayed
        asking the user whether the model should be created.
        """

        path = f"{os.getcwd()}"

        init = f"{path}/__init__.py"

        filename = model.lower()

        if not model.endswith('.py'):
            filename += '.py'

        if filename in os.listdir(path):
            return

        try:
            for line in fileinput.input(init):
                if model.capitalize() in line:
                    fileinput.close()
                    return
        except FileNotFoundError:
            pass

        fileinput.close()

        if click.confirm(DEFAULT_NOT_IN_SCOPE_WARNING.format(model.capitalize(), self.app_name)):
            self.dependencies_list.append(model.capitalize())

    def handle_dependencies(self, app, **kwargs):

        if len(self.dependencies_list) < 1:
            return False

        for model in self.dependencies_list:
            template = 'model.tpl'
            template_import = 'model-import.tpl'

            table_name = f"{app}_{inflection.pluralize(model)}"

            self.default_create(
                model,
                templates_directory=TEMPLATE_DIR,
                template=template,
                template_import=template_import,
                context={
                    'model': model,
                    'abstract': False,
                    'fields': [],
                    'imports': [],
                    'db_table': table_name,
                }
            )

        return True

    def append_import(self, value, scope=''):
        if value not in self.imports_list:
            self.imports_list.append([f'{scope}.{value}', f'{inflection.camelize(value)}'])

    def append_special_import(self, value, scope=''):
        """
        Creates an import statement for special inheritance.

        :param scope:
        :param value:
        :return:
        """
        if value in DEFAULT_SPECIAL_INHERITABLE_TYPES:
            statement = DEFAULT_SPECIAL_INHERITABLE_TYPES[value]
            value = inflection.camelize(inflection.underscore(value))
            self.special_import = (statement, value)
            return True
        else:
            model = inflection.camelize(inflection.underscore(value))
            value = inflection.underscore(value)
            if scope:
                if self.project_name:
                    self.special_import = (f'{self.project_name}.{scope}.models.{value}', model)
                else:
                    self.special_import = (f'{scope}.models.{value}', model)
            else:
                self.special_import = (f'.{value}', model)
        return False
