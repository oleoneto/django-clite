from .base import *
from djangocli.cli.templates.serializer import model_serializer


class SerializerHelper(BaseHelper):
    """
    TODO: Parse model to retrieve relationships
    Add such relationships to serializer class
    """
    def create(self, name, app='app'):
        return model_serializer.render(model=name, app=app)
    # end def
# end class
