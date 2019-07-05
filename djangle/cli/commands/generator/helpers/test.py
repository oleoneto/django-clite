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
