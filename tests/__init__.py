# tests
import unittest

from pathlib import Path

from cli import template_files
from geny.core.templates.template import TemplateParser

parser = TemplateParser(
    templates_dir=[Path(template_files.__file__).resolve().parent],
    context={},
)

if __name__ == "__main__":
    unittest.main()
