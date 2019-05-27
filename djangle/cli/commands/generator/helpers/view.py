from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.view import model_list_view, model_detail_view, function_based_view


class ViewHelper(BaseHelper):

    def create(self, *args, **kwargs):
        if kwargs['list']:
            return model_list_view.render(model=kwargs['name'])
        if kwargs['detail']:
            return model_detail_view.render(model=kwargs['name'])
        return function_based_view.render(name=kwargs['name'])
    # end def
# end class
