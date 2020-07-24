import os
import inflection
from cli.decorators import watch_templates
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.helpers import FSHelper


BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]


@watch_templates(os.path.join(BASE_DIR, 'templates'))
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
            templates_directory=self.TEMPLATES_DIRECTORY,
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
            templates_directory=self.TEMPLATES_DIRECTORY,
            template_import=template_import
        ):

            resource = f"{classname}Serializer"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

    def create_auth_user(self):
        self.create(
            model='User',
            template='serializer-user.tpl'
        )
