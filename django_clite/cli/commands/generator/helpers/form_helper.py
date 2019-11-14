import inflection
from django_clite.cli import log_success
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.form import (
    model_form_template,
    model_form_import_template
)


class FormHelper(BaseHelper):

    def create(self, **kwargs):

        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        path = kwargs['path']

        filename = f"{model.lower()}.py"

        self.parse_and_create(
            filename=filename,
            model=model,
            classname=kwargs['classname'],
            path=path,
            template=model_form_template,
            dry=kwargs['dry']
        )

        self.add_import(
            model=model,
            classname=kwargs['classname'],
            template=model_form_import_template,
            path=path,
            dry=kwargs['dry']
        )

        log_success('Successfully created form.')

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        filename = f"{model.lower()}.py"

        template = model_form_import_template

        if self.destroy(filename=filename, **kwargs):

            self.remove_import(template=template, **kwargs)

            log_success('Successfully deleted form.')

    @classmethod
    def create_auth_user(cls, **kwargs):
        cls.parse_and_create(
            filename=kwargs['filename'],
            model=kwargs['model'],
            path=kwargs['path'],
            template=model_form_template
        )

        cls.add_import(**kwargs, template=model_form_import_template)

# end class
