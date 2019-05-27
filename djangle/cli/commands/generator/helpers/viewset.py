from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.viewset import model_viewset


class ViewSetHelper(BaseHelper):

    def create(self, *args, **kwargs):
        return model_viewset.render(model=kwargs['name'], read_only=kwargs['read_only'])
    # end def
# end class
