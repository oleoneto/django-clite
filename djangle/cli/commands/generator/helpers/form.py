from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.form import model_form


class FormHelper(BaseHelper):
    def create(self, name):
        return model_form.render(model=name)
    # end def
# end class
