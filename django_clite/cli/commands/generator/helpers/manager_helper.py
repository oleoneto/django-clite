import inflection
from django_clite.cli import log_success
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.manager import (
    manager_template,
    manager_import_template
)


class ManagerHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        path = kwargs['path']

        filename = f"{model.lower()}.py"

        template = manager_template

        template_import = manager_import_template

        self.parse_and_create(
            filename=filename,
            model=model,
            classname=kwargs['classname'],
            path=path,
            template=template,
            dry=kwargs['dry']
        )

        self.add_import(**kwargs, template=template_import)

        log_success("Successfully created manager class.")

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        filename = f"{model.lower()}.py"

        template = manager_import_template

        if self.destroy(filename=filename, **kwargs):

            self.remove_import(template=template, **kwargs)

            log_success('Successfully deleted manager.')

# end class
