import inflection
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.commands.generate.helpers.generator import Generator


class TestHelper(Generator):

    def create(self, model, **kwargs):
        model = self.check_noun(model)
        model = sanitized_string(model)
        scope = kwargs.get('scope')

        template = f'{scope}-test.tpl' \
            if not kwargs.get('template') \
            else kwargs.get('template')
        template_import = 'test-import.tpl' \
            if not kwargs.get('template_import') \
            else kwargs.get('template_import')

        self.default_create(
            model,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template=template,
            template_import=template_import,
            scope='TestCase',
            context={
                'model': model,
                'namespace': inflection.pluralize(model)
            }
        )

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        filename = f"{model}.py"
        template_import = 'test-import.tpl'

        if self.default_destroy_file(
            model=model,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template_import=template_import
        ):

            resource = f"{classname}TestCase"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

    def create_auth_user(self, scope):
        self.create(
            model='user',
            scope=scope,
            template='model-test.tpl'
        )
