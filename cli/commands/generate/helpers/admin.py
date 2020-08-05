import inflection
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.commands.generate.helpers.generator import Generator


class AdminHelper(Generator):

    def create(self, model, **kwargs):
        model = sanitized_string(model)

        fields = kwargs.get('fields', None)
        inline = kwargs.get('inline', False)

        scope = "Admin"
        template = 'admin.tpl' \
            if not kwargs.get('template') \
            else kwargs.get('template')
        template_import = 'admin-import.tpl' \
            if not kwargs.get('template_import') \
            else kwargs.get('template_import')

        if inline:
            scope = "Inline"
            template = 'admin-inline.tpl'
            template_import = 'admin-inline-import.tpl'

        self.default_create(
            model,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template=template,
            template_import=template_import,
            scope=scope.capitalize(),
            context={'model': model, 'fields': fields, 'permissions': kwargs.get('permissions')}
        )

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        scope = "Admin"
        filename = f"{model.lower()}.py"
        template_import = 'admin-import.tpl'

        if kwargs['inline']:
            scope = "Inline"
            template_import = 'admin-inline-import.tpl'

        if self.default_destroy_file(
            model=model,
            templates_directory=self.TEMPLATES_DIRECTORY,
            template_import=template_import
        ):

            resource = f"{classname}{scope}"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

    def create_auth_user(self, **kwargs):
        self.create(
            model='User',
            inline=False,
            template='admin-user.tpl'
        )
