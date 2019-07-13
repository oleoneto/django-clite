from dj.cli import log_success
from dj.cli.commands.base_helper import BaseHelper
from dj.cli.templates.admin import (
    admin_user_auth_template,
    model_admin_import_template,
    model_admin_inline_template,
    model_admin_template,
    model_inline_import_template,
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

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        filename = f"{model.lower()}.py"

        template = model_admin_import_template

        message = "Successfully deleted admin model"

        if kwargs['inline']:
            template = model_inline_import_template
            message = "Successfully deleted admin inline"

        if self.destroy(filename=filename, **kwargs):
            self.remove_import(template=template, **kwargs)
            log_success(message)

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
