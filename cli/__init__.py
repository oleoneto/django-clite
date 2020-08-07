# coding: utf-8
"""
    django-clite: a cli tool that handles creating and managing Django projects
"""
from __future__ import unicode_literals
import os

__version__ = '0.15.1'
__license__ = 'BSD 3-Clause'
__copyright__ = 'Copyright 2019 Leo Neto'

COMMANDS_FOLDER = os.path.join(os.path.dirname(__file__), 'commands')

VERSION = __version__
