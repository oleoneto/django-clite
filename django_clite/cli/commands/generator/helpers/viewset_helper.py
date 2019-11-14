import inflection
from django_clite.cli import (
    log_success,
    DEFAULT_CREATE_MESSAGE,
    DEFAULT_DELETE_MESSAGE
)
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.viewset import (
    viewset_template,
    viewset_import_template
)


class ViewSetHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        path = kwargs['path']

        filename = f"{model.lower()}.py"

        # TODO: Ensure serializer already exists

        self.add_import(
            model=model,
            classname=kwargs['classname'],
            template=viewset_import_template,
            path=path,
            dry=kwargs['dry']
        )

        if self.parse_and_create(
            filename=filename,
            model=model,
            classname=kwargs['classname'],
            template=viewset_template,
            read_only=kwargs['read_only'],
            route=inflection.pluralize(model),
            path=path,
            dry=kwargs['dry']
        ):

            resource = f"{kwargs['classname']}ViewSet"
            log_success(DEFAULT_CREATE_MESSAGE.format(filename, resource))

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        filename = f"{model.lower()}.py"

        template = viewset_import_template

        if self.destroy(filename=filename, **kwargs):

            self.remove_import(template=template, **kwargs)

            resource = f"{kwargs['classname']}ViewSet"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

    @classmethod
    def create_auth_user(cls, **kwargs):

        # TODO: define create_auth_user() in terms of create()

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
