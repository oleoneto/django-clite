import inflection
from django_clite.cli import (
    log_success,
    DEFAULT_CREATE_MESSAGE,
    DEFAULT_DELETE_MESSAGE
)
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.admin import (
    admin_user_auth_template,
    model_admin_import_template,
    model_admin_inline_template,
    model_admin_template,
    model_inline_import_template,
)


class AdminHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        path = kwargs['path']

        filename = f"{model.lower()}.py"

        template = model_admin_template

        template_import = model_admin_import_template

        scope = "Admin"

        if kwargs['inline']:
            template = model_admin_inline_template
            template_import = model_inline_import_template
            scope = "Inline"

        self.add_import(**kwargs, template=template_import)

        if self.parse_and_create(
            filename=filename,
            model=model,
            classname=kwargs['classname'],
            path=path,
            template=template,
            dry=kwargs['dry']
        ):
            resource = f"{kwargs['classname']}{scope}"
            log_success(DEFAULT_CREATE_MESSAGE.format(filename, resource))

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        kwargs['classname'] = inflection.camelize(model)

        filename = f"{model.lower()}.py"

        template = model_admin_import_template

        scope = "Admin"

        if kwargs['inline']:
            template = model_inline_import_template
            scope = "Inline"

        if self.destroy(filename=filename, **kwargs):
            self.remove_import(template=template, **kwargs)
            resource = f"{kwargs['classname']}{scope}"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

    @classmethod
    def create_auth_user(cls, **kwargs):
        kwargs['model'] = 'User'

        kwargs['filename'] = 'user.py'

        kwargs['path'] = f"{kwargs['path']}/admin/"

        cls.parse_and_create(
            model=kwargs['model'],
            filename=kwargs['filename'],
            project_name=kwargs['project'],
            template=admin_user_auth_template,
            path=kwargs['path']
        )

        cls.add_import(**kwargs, template=model_admin_import_template)
# end class
