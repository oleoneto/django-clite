import os
import inflection
from django_clite.helpers.logger import *
from django_clite.helpers import sanitized_string
from django_clite.helpers import FieldParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class ModelHelper(FieldParser):

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
            if not self.append_special_import(base_model, scope=scope):
                self.find_resource_in_scope(base_model)

        # Get database name
        table_name = f"{self.app_name}_{inflection.pluralize(model)}"

        # Parse model fields by name and type
        if kwargs.get('fields') is not None:
            self.parse_fields(model, kwargs.get('fields'))

        # Handle SQL views
        # if is_sql:
        #     template = 'sql-model.tpl'

        self.default_create(
            model,
            templates_directory=TEMPLATE_DIR,
            template=template,
            template_import=template_import,
            context={
                'api': kwargs.get('api'),
                'abstract': kwargs.get('abstract'),
                'base': self.special_import,
                'fields': self.fields_list,
                'imports': self.imports_list,
                'db_table': table_name,
                'model': model,
                'model_plural': inflection.pluralize(model),
                'is_managed': kwargs.get('is_managed'),
                'soft_delete': kwargs.get('soft_delete'),
            }
        )

        # Ensure related models are created
        self.handle_dependencies(app=self.app_name, **kwargs)

        return self.admin_fields_list

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
