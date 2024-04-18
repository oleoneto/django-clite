# tests
import unittest

from pathlib import Path

from geny.core.templates.template import TemplateParser
from django_clite import template_files

parser = TemplateParser(
    templates_dir=[Path(template_files.__file__).resolve().parent],
    context={},
)

if __name__ == "__main__":
    unittest.main()
