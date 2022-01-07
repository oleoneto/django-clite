from rich import print as rich_print
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from cli.handlers.generic_handler import GenericHandler
from cli.decorators import watch_templates


@watch_templates()
class TemplateHandler(GenericHandler):
    def __init__(self, cwd='.', dry=False, force=False, verbose=False, debug=False, scope=None, context={}):
        super(TemplateHandler, self).__init__(cwd, dry, force, verbose, debug)
        self.scope = scope
        self.context = context

    def parsed_template(self, template, context={}, raw=False):
        self.context.update(context)

        try:
            if raw:
                return self.__parsed_template_string(template)
            return self.__parsed_template_file(template)
        except TemplateNotFound:
            return rich_print(f'Template [b]{template}[/b] does not exist.')

    def __parsed_template_file(self, template):
        templates_directory = f'{self.templates_directory}{self.scope if self.scope else ""}'
        environment = Environment(loader=FileSystemLoader(templates_directory), autoescape=select_autoescape())
        return environment.get_template(template).render(self.context)

    def __parsed_template_string(self, template):
        environment = Environment(autoescape=select_autoescape()).from_string(template)
        return environment.render(self.context)


# Aliases

ApplicationTemplateHandler = TemplateHandler(scope='app')
ProjectTemplateHandler = TemplateHandler(scope='project')
ResourceTemplateHandler = TemplateHandler(scope='resources')
SharedTemplateHandler = TemplateHandler(scope='shared')
TestTemplateHandler = TemplateHandler(scope='tests')
