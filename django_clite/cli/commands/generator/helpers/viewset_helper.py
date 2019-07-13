import inflection
from django_clite.cli import log_success
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.viewset import (
    viewset_template,
    viewset_import_template
)


class ViewSetHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        path = kwargs['path']

        filename = f"{model.lower()}.py"

        # TODO: Ensure serializer already exists

        self.parse_and_create(
            filename=filename,
            model=model,
            template=viewset_template,
            read_only=kwargs['read_only'],
            route=inflection.pluralize(model),
            path=path,
            dry=kwargs['dry']
        )

        self.add_import(
            model=model,
            template=viewset_import_template,
            path=path,
            dry=kwargs['dry']
        )

        log_success("Successfully created viewset.")

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        filename = f"{model.lower()}.py"

        template = viewset_import_template

        if self.destroy(filename=filename, **kwargs):

            self.remove_import(template=template, **kwargs)

            log_success('Successfully deleted viewset.')

    @classmethod
    def create_auth_user(cls, **kwargs):
        kwargs['model'] = 'User'

        kwargs['filename'] = 'user.py'

        kwargs['path'] = f"{kwargs['path']}/viewsets/"

        kwargs['route'] = inflection.pluralize(f"{kwargs['model']}")

        cls.parse_and_create(
            model=kwargs['model'],
            route=kwargs['route'],
            filename=kwargs['filename'],
            project_name=kwargs['project'],
            template=viewset_template,
            path=kwargs['path']
        )

        cls.add_import(**kwargs, template=viewset_import_template)

# end class
