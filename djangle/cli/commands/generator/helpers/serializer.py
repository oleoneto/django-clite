from djangle.cli import log_success
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.serializer import (
    model_serializer_template,
    model_serializer_import_template
)


class SerializerHelper(BaseHelper):

    def create(self, **kwargs):
        model = self.check_noun(kwargs['model'])

        path = kwargs['path']

        filename = f"{model.lower()}.py"

        template = model_serializer_template

        template_import = model_serializer_import_template

        self.parse_and_create(
            filename=filename,
            model=model,
            path=path,
            template=template,
            dry=kwargs['dry']
        )

        self.add_import(**kwargs, template=template_import)

        log_success("Successfully created serializer class")

# end class
