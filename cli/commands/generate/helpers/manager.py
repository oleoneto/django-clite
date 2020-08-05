import inflection
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.helpers import rendered_file_template
from cli.commands.generate.helpers.generator import Generator


class ManagerHelper(Generator):

    def create(self, model, **kwargs):

        model = self.check_noun(model)
        model = sanitized_string(model)
        classname = inflection.camelize(model)

        filename = f"{model.lower()}.py"

        template = 'manager.tpl'
        template_import = 'manager-import.tpl'

        content = rendered_file_template(
            path=self.TEMPLATES_DIRECTORY,
            template=template,
            context={'classname': classname, 'model': model}
        )

        import_content = rendered_file_template(
            path=self.TEMPLATES_DIRECTORY,
            template=template_import,
            context={'classname': classname, 'model': model}
        )

        self.add_import(
            template=template_import,
            content=import_content
        )

        if self.create_file(
            path=self.cwd,
            filename=filename,
            content=content
        ):

            resource = f"{classname}Manager"
            log_success(DEFAULT_CREATE_MESSAGE.format(filename, resource))

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        filename = f"{model}.py"
        template_import = 'manager-import.tpl'

        if self.default_destroy_file(
            model=model,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template_import=template_import
        ):

            resource = f"{classname}Manager"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))
