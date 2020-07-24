# {{ if project }}{{ project }}:{% endif %}{{ app }}:requires

"""
A list of all the apps this package requires to be installed in INSTALLED_APPS
In settings.py, do:

from {{ app }}.requires import REQUIRED_APPS

INSTALLED_APPS = [
    # django and other apps

    # this app here...
] + REQUIRED_APPS
"""

REQUIRED_APPS = []
