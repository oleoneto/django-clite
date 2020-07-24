import os
from cli.decorators import watch_templates
from cli.helpers import FSHelper
from cli.helpers import sanitized_string
from cli.helpers.logger import log_error


BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]


@watch_templates(os.path.join(BASE_DIR, 'templates'))
class SignalHelper(FSHelper):

    def create(self, name, **kwargs):
        name = sanitized_string(name)
        template = 'signal.tpl'
        template_import = 'generic-import.tpl'

        self.default_create(
            model=name,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template=template,
            template_import=template_import,
            context={'model': name}
        )

    def delete(self, name, **kwargs):
        name = sanitized_string(name)

        filename = f'{name}.py'
        template_import = 'generic-import.tpl'

        if self.default_destroy_file(
            model=name,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template_import=template_import
        ):

            log_error(f'Successfully deleted {filename}.')
