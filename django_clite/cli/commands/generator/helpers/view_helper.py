from django_clite.cli import log_success
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

        kwargs['model'] = model

        kwargs['name'] = model

        template = default_class_view_template

        template_import = default_class_view_import_template

        filename = f"{model.lower()}.py"

        if not kwargs['detail'] and not kwargs['list']:
            template = default_function_view_template
            template_import = default_function_view_import_template

        if kwargs['list']:
            filename = f"{model.lower()}_list.py"
        elif kwargs['detail']:
            filename = f"{model.lower()}_detail.py"

        self.parse_and_create(
            filename=filename,
            template=template,
            **kwargs
        )

        self.add_import(
            **kwargs,
            template=template_import,
        )

        log_success(f"Successfully created view.")

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        kwargs['model'] = model

        kwargs['name'] = model

        filename = f"{model.lower()}.py"

        if kwargs['list']:
            filename = f"{model.lower()}_list.py"
        elif kwargs['detail']:
            filename = f"{model.lower()}_detail.py"

        if self.destroy(filename=filename, **kwargs):

            if kwargs['list'] or kwargs['detail']:
                self.remove_import(
                    template=default_class_view_import_template,
                    model=model,
                    list=kwargs['list'],
                    detail=kwargs['detail'],
                    path=kwargs['path']
                )
            else:
                self.remove_import(template=default_function_view_import_template, **kwargs)

            log_success(f'Successfully deleted view.')

# end class
