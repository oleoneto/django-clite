import inflection
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.helpers import rendered_file_template
from cli.commands.generate.helpers.generator import Generator


class FixtureHelper(Generator):

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
            path=self.TEMPLATES_DIRECTORY,
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
            templates_directory=self.TEMPLATES_DIRECTORY
        ):

            resource = f"{classname} fixture"
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))
