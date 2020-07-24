import os
import inflection
from cli.decorators import watch_templates
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.helpers import rendered_file_template
from cli.helpers import FSHelper


BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]


@watch_templates(os.path.join(BASE_DIR, 'templates'))
class TemplateHelper(FSHelper):

    def create(self, model, **kwargs):

        model = sanitized_string(model)
        class_type = kwargs.get('class_type', None)
        page_title = inflection.camelize(model)

        template = 'template.tpl'
        filename = f"{model}.html"
        if class_type:
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
