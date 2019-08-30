import click
import fileinput
import inflection
import os
from django_clite.cli import log_success, sanitized_string, log_info
from django_clite.cli.commands.base_helper import BaseHelper
from django_clite.cli.templates.model import (
    model_field_template,
    model_import_template,
    model_template,
    sql_view_template
)

class SQLHelper(BaseHelper):
  pass
