# django-clite

A CLI tool that handles creating and managing Django projects

![PyPI - License](https://img.shields.io/pypi/l/django-clite?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-clite?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/django-clite?style=flat-square)
![Bitbucket Pipelines](https://img.shields.io/bitbucket/pipelines/oleoneto/django-clite/development?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-clite?style=flat-square)


- [Introduction](#django-clite)
- [Interactive Docs](#interactive-docs)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [To Do](#to-do)
- [Pull requests](#pull-requests)
- [LICENSE](#license)

## Interactive Docs
In order to maintain consistency in our documentation of all the different commands and features of the CLI,
 we've decided to move the [README](docs/cli/readme.ipynb) to a series of Jupyter notebooks which you can explore per command under the [docs](docs) directory.

## Dependencies
Check out [setup.py](setup.py) for all installation dependencies.

## Installation
Install via [pip](https://pypi.org/project/django-clite/):
```bash
pip install django-clite
```

Install from source:
```
git clone https://bitbucket.org/oleoneto/django-clite.git
cd django-clite
pip install .
```

After installation, the CLI will expose the binary with three names,
any of which can be used in place of the another:
```
D
django-clite
djc
```

## To Do
[Check out our open issues](/issues).

## Pull requests
Found a bug? See a typo? Have an idea for new command?
Feel free to submit a pull request with your contributions. They are much welcome and appreciated.

## LICENSE
**django-clite** is [BSD Licensed](LICENSE.txt).
