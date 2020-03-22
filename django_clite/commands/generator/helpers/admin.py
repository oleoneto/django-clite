import os
import inflection
from django_clite.helpers.logger import *
from django_clite.helpers import sanitized_string
from django_clite.helpers import FSHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class AdminHelper(FSHelper):

    def create(self, model, fields=None, **kwargs):
        model = sanitized_string(model)

        scope = "Admin"
        template = 'admin.tpl' \
            if not kwargs.get('template') \
            else kwargs.get('template')
        template_import = 'admin-import.tpl' \
            if not kwargs.get('template_import') \
            else kwargs.get('template_import')

        if kwargs['inline']:
            scope = "Inline"
            template = 'admin-inline.tpl'
            template_import = 'admin-inline-import.tpl'

        self.default_create(
            model,
            templates_directory=TEMPLATE_DIR,
            template=template,
            template_import=template_import,
            scope=scope.capitalize(),
            context={'model': model, 'fields': fields, 'permissions': kwargs.get('permissions')}
        )

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        scope = "Admin"
        filename = f"{model.lower()}.py"
        template_import = 'admin-import.tpl'

        if kwargs['inline']:
            scope = "Inline"
            template_import = 'admin-inline-import.tpl'

        if self.default_destroy_file(
            model=model,
            templates_directory=TEMPLATE_DIR,
            template_import=template_import
        ):

            resource = f"{classname}{scope}"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

    def create_auth_user(self, **kwargs):
        self.create(
            model='User',
            inline=False,
            template='admin-user.tpl'
        )
