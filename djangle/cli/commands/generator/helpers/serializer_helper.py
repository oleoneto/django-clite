from djangle.cli import log_success
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.serializer import (
    serializer_template,
    serializer_import_template,
    serializer_auth_user_template
)


class SerializerHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        path = kwargs['path']

        filename = f"{model.lower()}.py"

        template = serializer_template

        template_import = serializer_import_template

        self.parse_and_create(
            filename=filename,
            model=model,
            path=path,
            template=template,
            dry=kwargs['dry']
        )

        self.add_import(**kwargs, template=template_import)

        log_success("Successfully created serializer class.")

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        filename = f"{model.lower()}.py"

        template = serializer_import_template

        if self.destroy(filename=filename, **kwargs):

            self.remove_import(template=template, **kwargs)

            log_success('Successfully deleted serializer.')

    @classmethod
    def create_auth_user(cls, **kwargs):
        kwargs['model'] = 'User'

        kwargs['filename'] = 'user.py'

        kwargs['path'] = f"{kwargs['path']}/serializers/"

        cls.parse_and_create(
            model=kwargs['model'],
            filename=kwargs['filename'],
            project_name=kwargs['project'],
            template=serializer_auth_user_template,
            path=kwargs['path']
        )

        cls.add_import(**kwargs, template=serializer_import_template)

        log_success("Successfully created serializer class.")

# end class
