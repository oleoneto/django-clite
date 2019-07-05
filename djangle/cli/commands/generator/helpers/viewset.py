import inflection
from djangle.cli import log_success
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.viewset import (
    viewset_template,
    viewset_import_template
)


class ViewSetHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        path = kwargs['path']

        filename = f"{model.lower()}.py"

        # TODO: Ensure serializer already exists

        self.parse_and_create(
            filename=filename,
            model=model,
            template=viewset_template,
            read_only=kwargs['read_only'],
            route=inflection.pluralize(model),
            path=path,
            dry=kwargs['dry']
        )

        self.add_import(
            model=model,
            template=viewset_import_template,
            path=path,
            dry=kwargs['dry']
        )

        log_success("Successfully created viewset.")

# end class
