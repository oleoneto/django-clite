from djangocli.cli.commands.base_helper import BaseHelper
from djangocli.cli.templates.template import base_template


class TemplateHelper(BaseHelper):

    def create(self, name):
        return base_template.render(name=name)
    # end def
# end class
