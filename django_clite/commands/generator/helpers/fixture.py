import os
import inflection
from django_clite.helpers.logger import *
from django_clite.helpers import sanitized_string
from django_clite.helpers import rendered_file_template
from django_clite.helpers import FieldParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class FixtureHelper(FieldParser):

    def create(self, model, **kwargs):
        model = self.check_noun(model)
        model = sanitized_string(model)
        classname = inflection.camelize(model)

        if kwargs.get('fields') is not None:
            self.parse_fields(model, kwargs.get('fields'))

        template = 'fixture.tpl' \
            if not kwargs.get('template') \
            else kwargs.get('template')

        content = rendered_file_template(
            path=TEMPLATE_DIR,
            template=template,
            context={
                'total': int(kwargs.get('total')),
                'app': self.app_name,
                'classname': classname,
                'fields': self.fixture_fields,
            }
        )

        self.create_file(
            content=content,
            filename=f'{inflection.pluralize(model)}.json',
            path=self.cwd,
        )

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)

        filename = f"{model}.json"

        if self.default_destroy_file(
            model=model,
            templates_directory=TEMPLATE_DIR
        ):

            resource = f"{classname} fixture"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))
