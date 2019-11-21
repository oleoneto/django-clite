import os
import inflection
from django_clite.helpers.logger import *
from django_clite.helpers import sanitized_string
from django_clite.helpers import rendered_file_template
from django_clite.helpers import FSHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class ManagerHelper(FSHelper):

    def create(self, model, **kwargs):

        model = self.check_noun(model)
        model = sanitized_string(model)
        classname = inflection.camelize(model)

        filename = f"{model.lower()}.py"

        template = 'manager.tpl'
        template_import = 'manager-import.tpl'

        content = rendered_file_template(
            path=TEMPLATE_DIR,
            template=template,
            context={'classname': classname, 'model': model}
        )

        import_content = rendered_file_template(
            path=TEMPLATE_DIR,
            template=template_import,
            context={'classname': classname, 'model': model}
        )

        self.add_import(
            template=template_import,
            content=import_content
        )

        self.create_file(
            path=self.cwd,
            filename=filename,
            content=content
        )

        resource = f"{classname}Manager"
        log_success(DEFAULT_CREATE_MESSAGE.format(filename, resource))

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        filename = f"{model}.py"
        template_import = 'manager-import.tpl'

        if self.default_destroy_file(
            model=model,
            templates_directory=TEMPLATE_DIR,
            template_import=template_import
        ):

            resource = f"{classname}Manager"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))
