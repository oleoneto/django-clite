import os
from django_clite.helpers.logger import *
from django_clite.helpers import sanitized_string
from django_clite.helpers import rendered_file_template
from django_clite.helpers import FSHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class TemplateHelper(FSHelper):

    def create(self, model, **kwargs):

        model = sanitized_string(model)

        template = 'template.tpl'
        filename = f"{model}.html"
        if kwargs.get('class_type'):
            filename = f"{model.lower()}_{kwargs.get('class_type')}.html"

        content = rendered_file_template(
            path=TEMPLATE_DIR,
            template=template,
            context={}
        )

        self.create_file(
            path=self.cwd,
            filename=filename,
            content=content
        )

        log_success(f"Successfully created {filename} template.")

    def delete(self, model, **kwargs):
        model = self.check_noun(model)

        filename = f"{model.lower()}.html"

        if self.destroy_file(filename=filename, **kwargs):
            log_success(f"Successfully deleted {filename} template.")
