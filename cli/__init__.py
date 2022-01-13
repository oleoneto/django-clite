# coding: utf-8
"""
    django-clite: a cli tool that handles creating and managing Django projects
"""
from __future__ import unicode_literals
import os

__version__ = '0.16.0'
__license__ = 'BSD 3-Clause'
__author__ = 'Leo Neto'
__copyright__ = 'Copyright 2019 Leo Neto'

COMMANDS_FOLDER = os.path.join(os.path.dirname(__file__), 'commands')  # use an array so the path can be extended

VERSION = __version__
