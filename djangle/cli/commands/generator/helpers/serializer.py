from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.serializer import model_serializer


class SerializerHelper(BaseHelper):
    """
    TODO: Parse model to retrieve relationships
    Add such relationships to serializer class
    """
    def create(self, *args, **kwargs):
        return model_serializer.render(model=kwargs['name'])
    # end def
# end class
