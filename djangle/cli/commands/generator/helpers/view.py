from djangle.cli import log_success
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.view import (
    function_view_template,
    view_import_template,
    view_template,
)


class ViewHelper(BaseHelper):

    def create(self, **kwargs):
        model = kwargs['name']

        path = kwargs['path']

        template = view_template

        if kwargs['detail']:
            generic_view_type = 'detail'
            model = self.check_noun(model)
            view_type = 'DetailView'
            view_name = f"{model.capitalize()}{view_type}"
            filename = f"{model.lower()}.py"
        elif kwargs['list']:
            generic_view_type = 'list'
            model = self.check_noun(model)
            view_type = 'ListView'
            view_name = f"{model.capitalize()}{view_type}"
            filename = f"{model.lower()}.py"
        else:
            generic_view_type = None
            view_type = '_view'
            view_name = f"{kwargs['name'].lower()}{view_type}"
            template = function_view_template
            filename = f"{model.lower()}.py"

        self.parse_and_create(
            filename=filename,
            model=model,
            path=path,
            template=template,
            generic_view_type=generic_view_type,
            view_type=view_type,
            view_name=view_name,
            dry=kwargs['dry']
        )

        self.add_import(
            **kwargs,
            view_file=kwargs['name'],
            view_name=view_name,
            template=view_import_template,
        )

        log_success(f"Successfully created {view_name}")

# end class
