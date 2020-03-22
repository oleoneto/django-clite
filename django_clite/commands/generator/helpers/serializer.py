import os
import inflection
from django_clite.helpers.logger import *
from django_clite.helpers import sanitized_string
from django_clite.helpers import FSHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class SerializerHelper(FSHelper):

    def create(self, model, **kwargs):
        model = sanitized_string(model)

        template = 'serializer.tpl' \
            if not kwargs.get('template') \
            else kwargs.get('template')
        template_import = 'serializer-import.tpl' \
            if not kwargs.get('template_import') \
            else kwargs.get('template_import')

        self.default_create(
            model,
            templates_directory=TEMPLATE_DIR,
            template=template,
            template_import=template_import,
            scope='Serializer',
            context={'model': model}
        )

    def delete(self, model):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        filename = f"{model}.py"
        template_import = 'serializer-import.tpl'

        if self.default_destroy_file(
            model=model,
            templates_directory=TEMPLATE_DIR,
            template_import=template_import
        ):

            resource = f"{classname}Serializer"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

    def create_auth_user(self):
        self.create(
            model='User',
            template='serializer-user.tpl'
        )
