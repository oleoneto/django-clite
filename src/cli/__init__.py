# coding: utf-8
"""
    django-clite: a cli tool that handles creating and managing Django projects
"""
import os

__version__ = "0.18.0"
__license__ = "BSD 3-Clause"
__author__ = "Leo Neto"
__copyright__ = "Copyright 2019-2023 Leo Neto"

COMMANDS_FOLDER = os.path.join(os.path.dirname(__file__), "commands")

PLUGINS_FOLDER = os.environ.get("DJANGO_CLITE_PLUGINS", None)

VERSION = __version__
