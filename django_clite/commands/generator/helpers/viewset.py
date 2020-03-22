import os
import inflection
from django_clite.helpers.logger import *
from django_clite.helpers import sanitized_string
from django_clite.helpers import rendered_file_template
from django_clite.helpers import FSHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class ViewSetHelper(FSHelper):

    def create(self, model, read_only=False):
        model = sanitized_string(model)

        template = 'viewset.tpl'
        template_import = 'viewset-import.tpl'

        # TODO: Ensure serializer already exists

        self.default_create(
            model,
            templates_directory=TEMPLATE_DIR,
            template=template,
            template_import=template_import,
            scope='ViewSet',
            context={
                'model': model,
                'read_only': read_only,
                'route': inflection.pluralize(model),
            }
        )

    def delete(self, model):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        filename = f"{model}.py"
        template_import = 'viewset-import.tpl'

        if self.default_destroy_file(
            model=model,
            templates_directory=TEMPLATE_DIR,
            template_import=template_import
        ):

            resource = f"{classname}ViewSet"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))
