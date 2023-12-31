# tests:core:templates
from pathlib import Path
from cli.core.templates.template import TemplateParser

TemplateParser(
    templates_dir=Path("temp/"),
    context={},
)
