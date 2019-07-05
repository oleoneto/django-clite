from djangle.cli import log_success
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.template import page_template


class TemplateHelper(BaseHelper):

    def create(self, **kwargs):
        filename = f"{kwargs['name'].lower()}.html"

        template = page_template

        path = kwargs['path']

        self.parse_and_create(
            filename=filename,
            name=kwargs['name'],
            path=path,
            template=template,
            dry=kwargs['dry']
        )

        log_success("Successfully created HTML template")

# end class
