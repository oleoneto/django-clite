import os
from djangocli.cli.commands.base_helper import BaseHelper
from djangocli.cli.templates.admin import model_admin, model_import, model_admin_inline


class AdminHelper(BaseHelper):

    def create(self, *args, **kwargs):
        return model_admin.render(model=kwargs['name'])
    # end def

    def create_inline(self, *args, **kwargs):
        return model_admin_inline.render(model=kwargs['name'])
    # end def

    def create_in_init(self, **kwargs):
        content = model_import.render(model=kwargs['name'])

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
