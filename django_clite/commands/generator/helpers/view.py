import os
import inflection
from django_clite.helpers.logger import *
from django_clite.helpers import sanitized_string
from django_clite.helpers import rendered_file_template
from django_clite.helpers import FSHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class ViewHelper(FSHelper):

    def create(self, model, class_type, **kwargs):
        model = self.check_noun(model)
        model = sanitized_string(model)
        classname = inflection.camelize(model)

        filename = f"{model.lower()}.py"
        template = 'view-function.tpl'
        template_import = 'view-function-import.tpl'

        if class_type is not None:
            filename = f"{model.lower()}_{class_type}.py"
            template = 'view-class.tpl'
            template_import = 'view-class-import.tpl'

        content = rendered_file_template(
            path=TEMPLATE_DIR,
            template=template,
            context={
                'model': model,
                'classname': classname,
                'class_type': class_type
            }
        )

        import_content = rendered_file_template(
            path=TEMPLATE_DIR,
            template=template_import,
            context={
                'model': model,
                'classname': classname,
                'class_type': class_type,
            }
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

        resource = f"{model}_view."
        if class_type:
            resource = f"{classname}{class_type.capitalize()}View."
        log_success(DEFAULT_CREATE_MESSAGE.format(filename, resource))

    def delete(self, model, class_type, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        filename = f"{model}.py"
        template_import = 'view-function-import.tpl'

        if class_type is not None:
            filename = f"{model}_{class_type}.py"
            template_import = 'view-class-import.tpl'

        content = rendered_file_template(
            path=TEMPLATE_DIR,
            template=template_import,
            context={
                'model': model,
                'classname': classname,
                'class_type': class_type,
            }
        )

        self.remove_import(content=content)

        if self.destroy_file(
            filename=filename,
            path=self.cwd
        ):

            resource = f"{model}_view."
            if class_type:
                resource = f"{classname}{class_type.capitalize()}View."
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

        return True
