import os
from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.admin import model_admin, model_admin_import, model_admin_inline, model_inline_import


class AdminHelper(BaseHelper):

    def create(self, *args, **kwargs):
        return model_admin.render(model=kwargs['name'])
    # end def

    def create_inline(self, *args, **kwargs):
        return model_admin_inline.render(model=kwargs['name'])
    # end def

    def add_admin_inline_import_to_init(self, **kwargs):
        content = model_inline_import.render(model=kwargs['name'])

        try:
            os.chdir(kwargs['path'])

            with open('__init__.py', 'a') as file:
                file.write(content)
                file.write('\n')
            file.close()
        except FileNotFoundError:
            raise FileNotFoundError
        return content

    # end def

    def add_admin_import_to_init(self, **kwargs):
        content = model_admin_import.render(model=kwargs['name'])

        try:
            os.chdir(kwargs['path'])

            with open('__init__.py', 'a') as file:
                file.write(content)
                file.write('\n')
            file.close()
        except FileNotFoundError:
            raise FileNotFoundError
        return content
    # end def
# end class
