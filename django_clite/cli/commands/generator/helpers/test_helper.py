import inflection
from django_clite.cli import log_success
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.test import (
    test_model_template,
    test_serializer_template,
    test_import_template
)


class TestHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])
        classname = inflection.camelize(model)

        path = kwargs['path']
        template = test_model_template
        namespace = inflection.pluralize(model)

        if kwargs['scope'] == 'serializer':
            template = test_serializer_template

        filename = f"{model}.py"

        self.parse_and_create(
            model=model,
            classname=classname,
            namespace=namespace,
            filename=filename,
            template=template,
            path=path,
            dry=kwargs['dry']
        )

        self.add_import(
            model=model,
            classname=classname,
            template=test_import_template,
            path=path
        )

        log_success("Successfully created TestCase.")

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        filename = f"{model.lower()}.py"

        template = test_import_template

        if self.destroy(filename=filename, **kwargs):

            self.remove_import(template=template, **kwargs)

            log_success('Successfully deleted TestCase.')

    @classmethod
    def create_auth_user(cls, **kwargs):
        # TODO: Define create_auth_user() in terms of create()

        kwargs['model'] = 'User'

        kwargs['filename'] = 'user.py'

        path = kwargs['path']

        namespace = inflection.pluralize(kwargs['model'])

        kwargs['path'] = f"{path}/models/tests/"
        cls.parse_and_create(
            model=kwargs['model'],
            filename=kwargs['filename'],
            project_name=kwargs['project'],
            template=test_model_template,
            path=kwargs['path']
        )
        cls.add_import(**kwargs, template=test_import_template)

        kwargs['path'] = f"{path}/serializers/tests/"
        cls.parse_and_create(
            model=kwargs['model'],
            namespace=namespace,
            filename=kwargs['filename'],
            project_name=kwargs['project'],
            template=test_serializer_template,
            path=kwargs['path']
        )
        cls.add_import(**kwargs, template=test_import_template)

        log_success("Successfully created TestCase.")
