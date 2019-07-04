from djangle.cli.commands.base_helper import BaseHelper
from djangle.cli.templates.viewset import model_viewset
from inflect import engine as inflection_engine


class ViewSetHelper(BaseHelper):

    def create(self, *args, **kwargs):

        engine = inflection_engine()

        model_plural_name = engine.plural(kwargs['name'])
        return model_viewset.render(model=kwargs['name'], route=model_plural_name, read_only=kwargs['read_only'])
    # end def
# end class
