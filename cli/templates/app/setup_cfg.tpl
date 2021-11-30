[metadata]
name = {{ app }}
description = {{ description }}
long_description = file: README.md
url = {{ url }}
author = {{ author }}
author_email = {{ email }}
license = BSD-3-Clause
keywords = django
classifiers =
    Environment :: Web Environment
    Framework :: Django
    Framework :: Django :: 2.2
    Framework :: Django :: 3.0
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Operating System :: OS Independent
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8
    Topic :: Internet :: WWW/HTTP
    Topic :: Internet :: WWW/HTTP :: Dynamic Content

[options]
include_package_data = true
packages = find:
install_requires =
    django>=2.2
