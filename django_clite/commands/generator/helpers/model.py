import os
import fileinput
import inflection
from django_clite.helpers.logger import *
from django_clite.helpers import sanitized_string
from django_clite.helpers import rendered_file_template
from django_clite.helpers import get_project_name
from django_clite.helpers import FSHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]

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
    'URLField': '',
    'UUIDField': 'default=uuid.uuid4, editable=False',
}

DEFAULT_SPECIAL_INHERITABLE_TYPES = {
    'abstract-user': 'django.contrib.auth.models',
    'abstract-base-user': 'django.contrib.auth.models',
    'base-user': 'django.contrib.auth.models',
    'user': 'django.contrib.auth.models',
}


class ModelHelper(FSHelper):

    # List of fields to be rendered in model template
    fields_list = []

    # List models referred to in ForeignKey, OneToOne, or ManyToMany fields.
    dependencies_list = []

    # List of imports to be rendered in model template
    imports_list = []

    # List of special imports to be rendered in model template
    special_import = []

    ####################################

    def create(self, model, is_sql=False, **kwargs):
        model = sanitized_string(model)
        template = 'model.tpl' \
            if not kwargs.get('template') \
            else kwargs.get('template')
        template_import = 'model-import.tpl'

        # Get name of the parent class for this model (if any)
        base_model = self.check_noun(kwargs['inherits']) if kwargs['inherits'] else None
        scope = kwargs.get('scope', '')

        self.project_name = kwargs.get('project') if kwargs.get('project') else self.project_name

        # Check if model is in the `special` category before
        # attempting to create a module for it if one is not found.
        if base_model is not None:
            if not self.__append_special_import(base_model, scope=scope):
                self.__find_resource_in_scope(base_model)

        # Get app name
        app = self.__get_app_name()

        # Get database name
        table_name = f"{app}_{inflection.pluralize(model)}"

        # Parse model fields by name and type
        if kwargs['fields'] is not None:
            self.__parse_fields(model, **kwargs)

        # Handle SQL views
        # if is_sql:
        #     template = 'sql-model.tpl'

        self.default_create(
            model,
            templates_directory=TEMPLATE_DIR,
            template=template,
            template_import=template_import,
            context={
                'abstract': kwargs.get('abstract'),
                'base': self.special_import,
                'fields': self.fields_list,
                'imports': self.imports_list,
                'db_table': table_name,
                'model': model
            }
        )

        # Ensure related models are created
        self.__handle_dependencies(app=app, **kwargs)

        return

    ####################################

    def __handle_tokens(self, field):
        """
        Should parse input attribute into individual tokens.
        Expect input to be of the form (char:name, text:bio, image:artwork)

        :param field: model field to be parsed
        :return:
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

    def __handle_field(self, model, field_name, field_type):
        """
        Determines what options are present with each model field.

        :param model: the current model
        :param field_name: name of model field. i.e. first_name
        :param field_type: type of model field. i.e. CharField
        :return:
        """

        if DEFAULT_MODEL_OPTIONS[field_type] is not None:
            template = 'model-field.tpl'

            if field_type == "ForeignKey":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(
                    field_name.capitalize(),
                    inflection.pluralize(model.lower())
                )
                self.__find_resource_in_scope(field_name)
                self.__append_import(field_name)

            elif field_type == "OneToOneField":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(
                    field_name.capitalize(),
                    inflection.singularize(model)
                )
                self.__find_resource_in_scope(field_name)
                self.__append_import(field_name)

            elif field_type == "ManyToManyField":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(
                    field_name.capitalize()
                )
                self.__find_resource_in_scope(field_name)
                self.__append_import(field_name)

            elif field_type == "FileField" or "ImageField":
                options = DEFAULT_MODEL_OPTIONS[field_type].format(inflection.pluralize(field_name))

            else:
                options = DEFAULT_MODEL_OPTIONS[field_type]

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

    def __parse_fields(self, model, fields, **kwargs):
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

    ####################################

    def __find_resource_in_scope(self, model):
        """
        Searches the current directory for the specified model
        either by filename or import statement in __init__.py

        If the model is not found in the current scope, a warning is displayed
        asking the user whether the model should be created.
        """

        path = f"{os.getcwd()}/models"

        init = f"{path}/__init__.py"

        app_name = self.__get_app_name()

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

        if click.confirm(DEFAULT_NOT_IN_SCOPE_WARNING.format(model.capitalize(), app_name)):
            self.dependencies_list.append(model.capitalize())

    def __handle_dependencies(self, app, **kwargs):

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

    def __append_import(self, value, scope=''):
        if value not in self.imports_list:
            self.imports_list.append([f'{scope}.{value}', f'{inflection.camelize(value)}'])

    def __append_special_import(self, value, scope=''):
        """
        Creates an import statement for special inheritance.

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

    ####################################

    @classmethod
    def __get_app_name(cls):
        """
        Searches current directory for apps.py in order to
        retrieve the application name from it.
        """
        try:
            for line in fileinput.input('apps.py'):
                if "name = " in line:
                    fileinput.close()
                    return line.split(" = ")[-1]\
                        .lstrip()\
                        .replace("\n", "")\
                        .replace("'", "")\
                        .split('.')[-1]
            fileinput.close()
        except FileNotFoundError:
            return "app"
        return "app"

    ####################################

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        filename = f"{model}.py"
        template_import = 'model-import.tpl'

        if self.default_destroy_file(
            model=model,
            templates_directory=TEMPLATE_DIR,
            template_import=template_import
        ):

            resource = f"{classname}"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

    def create_auth_user(self):
        self.create(
            model='user',
            inherits=None,
            fields=None,
            template='model-user.tpl'
        )
