import inflection
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.helpers import rendered_file_template
from cli.commands.generate.helpers.generator import Generator


MODEL_VIEWS = ['create', 'detail', 'update', 'delete', 'list']

CHANGE_VIEWS = ['update', 'delete']

RECORD_VIEWS = ['update', 'delete', 'detail']


class TemplateHelper(Generator):

    def create(self, model, **kwargs):

        model = sanitized_string(model)
        class_type = kwargs.get('class_type', None)
        page_title = inflection.camelize(model)

        template = 'template.tpl'
        filename = f"{model}.html"

        if class_type is not None:
            if class_type in MODEL_VIEWS:
                filename = f"{model.lower()}_{class_type}.html"
                template = f"template_{class_type}.tpl"

            if class_type == 'list':
                page_title = inflection.pluralize(model)

        content = rendered_file_template(
            path=self.TEMPLATES_DIRECTORY,
            template=template,
            context={
                'page_title': page_title
            }
        )

        self.create_file(
            path=self.cwd,
            filename=filename,
            content=content
        )

        log_success(f"Successfully created {filename} template.")

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        class_type = kwargs.get('class_type', None)

        filename = f"{model.lower()}.html"

        if class_type:
            filename = f"{model.lower()}_{class_type}.html"

        if self.destroy_file(filename=filename, **kwargs):
            log_success(f"Successfully deleted {filename} template.")
