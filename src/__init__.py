# coding: utf-8
"""
    django-clite: a cli tool that handles creating and managing Django projects
"""
import os
from django_clite.constants import PLUGINS_ENV_VAR

__license__ = "BSD 3-Clause"
__author__ = "Leo Neto"
__copyright__ = "Copyright 2019-2023 Leo Neto"

COMMANDS_FOLDER = os.path.join(os.path.dirname(__file__), "commands")

PLUGINS_FOLDER = os.environ.get(PLUGINS_ENV_VAR, None)
