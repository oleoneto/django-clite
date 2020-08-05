import inflection
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.commands.generate.helpers.generator import Generator


class IndexHelper(Generator):

    def create(self, model, **kwargs):
        model = sanitized_string(model)
        template = 'index.tpl'
        template_import = 'index-import.tpl'
        classname = inflection.camelize(model)
        text_template = kwargs.get('template')

        self.default_create(
            model=model,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template=template,
            template_import=template_import,
            context={
                'model': model,
                'classname': classname,
                'app': self.app_name,
                'template': text_template,
            }
        )

        # TODO: Generate template files

    def delete(self, model, **kwargs):
        name = sanitized_string(model)

        filename = f'{name}.py'
        template_import = 'index-import.tpl'

        if self.default_destroy_file(
            model=name,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template_import=template_import
        ):

            log_error(f'Successfully deleted {filename}.')
