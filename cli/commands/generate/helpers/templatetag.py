from cli.helpers import sanitized_string
from cli.helpers.logger import log_error
from cli.commands.generate.helpers.generator import Generator


class TemplateTagHelper(Generator):

    def create(self, model, **kwargs):
        name = sanitized_string(model)
        template = 'templatetag.tpl'
        template_import = 'generic-import.tpl'

        self.default_create(
            model=name,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template=template,
            template_import=template_import,
            context={'model': name}
        )

    def delete(self, model, **kwargs):
        name = sanitized_string(model)

        filename = f'{name}.py'
        template_import = 'generic-import.tpl'

        if self.default_destroy_file(
            model=name,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template_import=template_import
        ):

            log_error(f'Successfully deleted {filename}.')
