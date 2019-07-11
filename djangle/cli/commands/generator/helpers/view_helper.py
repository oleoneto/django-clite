from djangle.cli import log_success
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.view import (
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

        if self.destroy(filename=filename, **kwargs):

            self.remove_import(
                template=default_class_view_import_template,
                model=model,
                list=True,
                path=kwargs['path']
            )

            self.remove_import(
                template=default_class_view_import_template,
                model=model,
                detail=True,
                path=kwargs['path']
            )

            self.remove_import(template=default_function_view_import_template, **kwargs)

            log_success(f'Successfully deleted view.')

# end class
