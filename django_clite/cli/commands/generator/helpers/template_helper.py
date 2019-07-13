<<<<<<< HEAD:django_clite/cli/commands/generator/helpers/template_helper.py
from django_clite.cli import log_success
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.template import page_template
=======
from dj.cli import log_success
from dj.cli.commands.base_helper import BaseHelper
from dj.cli.templates.template import page_template
>>>>>>> cdd5ae1b06170474ce89ba48faaf0c847c938c34:dj/cli/commands/generator/helpers/template_helper.py


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

        log_success("Successfully created HTML template.")

    def delete(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        filename = f"{model.lower()}.html"

        if self.destroy(filename=filename, **kwargs):

            log_success('Successfully deleted HTML template.')

# end class
