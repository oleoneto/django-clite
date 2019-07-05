from djangle.cli import log_success
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.admin import (
    model_admin_import_template,
    model_admin_inline_template,
    model_admin_template,
    model_inline_import_template
)


class AdminHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        path = kwargs['path']

        filename = f"{model.lower()}.py"

        template = model_admin_template

        template_import = model_admin_import_template

        message = "Successfully created admin model"

        if kwargs['inline']:
            template = model_admin_inline_template
            template_import = model_inline_import_template
            message = "Successfully created admin inline"

        self.parse_and_create(
            filename=filename,
            model=model,
            path=path,
            template=template,
            dry=kwargs['dry']
        )

        self.add_import(**kwargs, template=template_import)

        log_success(message)

# end class
