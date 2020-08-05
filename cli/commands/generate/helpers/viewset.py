import inflection
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.commands.generate.helpers.generator import Generator


class ViewSetHelper(Generator):

    def create(self, model, **kwargs):
        model = sanitized_string(model)

        template = 'viewset.tpl'
        template_import = 'viewset-import.tpl'
        read_only = kwargs.get('read_only', None)

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

    def delete(self, model, **kwargs):
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
