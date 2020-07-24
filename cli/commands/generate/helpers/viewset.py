import os
import inflection
from cli.decorators import watch_templates
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.helpers import FSHelper


BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]


@watch_templates(os.path.join(BASE_DIR, 'templates'))
class ViewSetHelper(FSHelper):

    def create(self, model, read_only=False):
        model = sanitized_string(model)

        template = 'viewset.tpl'
        template_import = 'viewset-import.tpl'

        # TODO: Ensure serializer already exists

        self.default_create(
            model,
            templates_directory=self.TEMPLATES_DIRECTORY,
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
            templates_directory=self.TEMPLATES_DIRECTORY,
            template_import=template_import
        ):

            resource = f"{classname}ViewSet"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))
