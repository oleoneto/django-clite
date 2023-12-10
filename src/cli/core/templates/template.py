# cli:core:templates
from .protocols import TemplateParserProtocol
from jinja2 import Environment, FileSystemLoader, select_autoescape
from cli.decorators.singleton import singleton


@singleton
class TemplateParser(TemplateParserProtocol):
    def __init__(self, templates_dir, context):
        self.project = context.get("project", "")
        self.app = context.get("app", "")
        self.context = context
        self.template_directories = templates_dir

    def parse_file(self, filepath, variables) -> str:
        self.context.update(variables)

        environment = Environment(
            loader=FileSystemLoader(self.template_directories),
            autoescape=select_autoescape(),
        )

        return environment.get_template(filepath).render(self.context)

    def parse_string(self, content, variables) -> str:
        self.context.update(variables)

        environment = Environment(autoescape=select_autoescape()).from_string(content)
        return environment.render(self.context)
