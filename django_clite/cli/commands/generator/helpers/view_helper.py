import inflection
from django_clite.cli import (
    log_success,
    DEFAULT_CREATE_MESSAGE,
    DEFAULT_DELETE_MESSAGE
)
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.view import (
    default_function_view_template,
    default_function_view_import_template,
    default_class_view_template,
    default_class_view_import_template
)


class ViewHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        kwargs['model'] = model

        filename = f"{model.lower()}.py"
        template = default_function_view_template
        template_import = default_function_view_import_template

        if kwargs['class_type'] is not None:
            filename = f"{model.lower()}_{kwargs['class_type']}.py"
            template = default_class_view_template
            template_import = default_class_view_import_template

        self.add_import(**kwargs, template=template_import)

        if self.parse_and_create(filename=filename, template=template, **kwargs):
            resource = f"{model}_view."
            if kwargs['class_type']:
                resource = f"{kwargs['classname']}{kwargs['class_type'].capitalize()}View."
            log_success(DEFAULT_CREATE_MESSAGE.format(filename, resource))

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        kwargs['model'] = model

        filename = f"{model.lower()}.py"
        kwargs['template'] = default_function_view_template
        template_import = default_function_view_import_template

        if kwargs['class_type'] is not None:
            filename = f"{model.lower()}_{kwargs['class_type']}.py"
            kwargs['template'] = default_class_view_template
            template_import = default_class_view_import_template

        if self.destroy(filename=filename, **kwargs):
            kwargs.pop('template')

            self.remove_import(
                template=template_import,
                **kwargs
            )

            resource = f"{model}_view."

            if kwargs['class_type']:
                resource = f"{kwargs['classname']}{kwargs['class_type'].capitalize()}View."

            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

# end class
