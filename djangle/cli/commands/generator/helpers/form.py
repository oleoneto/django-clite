from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.form import (
    model_form_template,
    model_form_import_template
)


class FormHelper(BaseHelper):
    def create(self, **kwargs):

        model = self.check_noun(kwargs['model'])
        path = kwargs['path']

        filename = f"{model.lower()}.py"

        self.parse_and_create(
            filename=filename,
            model=model,
            path=path,
            template=model_form_template,
            dry=kwargs['dry']
        )

        self.add_import(
            model=model,
            template=model_form_import_template,
            path=path,
            dry=kwargs['dry']
        )

# end class
