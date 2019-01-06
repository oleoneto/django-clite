from .base import *
from djangocli.cli.templates.viewset import __viewset__ as vs_


class ViewSetHelper(BaseHelper):

    def create(self, name, app='app', read_only=False):
        return vs_.render(model=name, app=app, read_only=read_only)
    # end def
# end class
