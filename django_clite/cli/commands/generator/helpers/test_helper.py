<<<<<<< HEAD:django_clite/cli/commands/generator/helpers/test_helper.py
from django_clite.cli import log_success
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.test import test_case_template, test_case_import_template
=======
from dj.cli import log_success
from dj.cli.commands.base_helper import BaseHelper
from dj.cli.templates.test import test_case_template, test_case_import_template
>>>>>>> cdd5ae1b06170474ce89ba48faaf0c847c938c34:dj/cli/commands/generator/helpers/test_helper.py


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

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        filename = f"{model.lower()}.py"

        template = test_case_import_template

        if self.destroy(filename=filename, **kwargs):

            self.remove_import(template=template, **kwargs)

            log_success('Successfully deleted TestCase.')

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
