# coding: utf-8
"""
    {{ app }}
"""
from __future__ import unicode_literals
from .requires import REQUIRED_APPS

__version__ = '{{ version }}'
__license__ = '{{ license }}'
__copyright__ = '{{ copyright }}'

VERSION = __version__

default_app_config = '{% if package %}{{ app }}{% endif %}.apps.{{ classname }}Config'
