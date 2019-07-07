from djangle.cli import log_success
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.test import test_case_template, test_case_import_template


class TestHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        path = kwargs['path']

        filename = f"{model}.py"

        self.parse_and_create(
            model=model,
            filename=filename,
            template=test_case_template,
            path=path,
            dry=kwargs['dry']
        )

        self.add_import(
            model=model,
            template=test_case_import_template,
            path=path
        )

        log_success("Successfully created TestCase.")

    @classmethod
    def create_auth_user(cls, **kwargs):
        kwargs['model'] = 'User'

        kwargs['filename'] = 'user.py'

        kwargs['path'] = f"{kwargs['path']}/tests/"

        cls.parse_and_create(
            model=kwargs['model'],
            filename=kwargs['filename'],
            project_name=kwargs['project'],
            template=test_case_template,
            path=kwargs['path']
        )

        cls.add_import(**kwargs, template=test_case_import_template)

        log_success("Successfully created TestCase.")
