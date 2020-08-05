import inflection
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.commands.generate.helpers.generator import Generator


class FormHelper(Generator):

    def create(self, model, **kwargs):
        model = sanitized_string(model)

        template = 'form.tpl' \
            if not kwargs.get('template') \
            else kwargs.get('template')
        template_import = 'form-import.tpl' \
            if not kwargs.get('template_import') \
            else kwargs.get('template_import')

        self.default_create(
            model,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template=template,
            template_import=template_import,
            scope='Form',
            context={'model': model}
        )

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        filename = f"{model}.py"
        template_import = 'form-import.tpl'

        if self.default_destroy_file(
            model=model,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template_import=template_import
        ):

            resource = f"{classname}Form"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

    def create_auth_user(self, **kwargs):
        self.create(
            model='User',
            template='form-user.tpl'
        )
