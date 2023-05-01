# django-clite

A CLI tool that handles creating and managing Django projects

![publish](https://github.com/oleoneto/django-clite/workflows/publish/badge.svg?branch=master)
![PyPI - Package](https://img.shields.io/pypi/v/django-clite)
![PyPI - Python](https://img.shields.io/pypi/pyversions/django-clite)
![PyPI - License](https://img.shields.io/pypi/l/django-clite)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-clite)


- [django-clite](#django-clite)
  - [Installation](#installation)
    - [Extending the CLI](#extending-the-cli)
  - [Dependencies](#dependencies)
  - [Interactive Docs](#interactive-docs)
  - [To Do](#to-do)
  - [Pull requests](#pull-requests)
  - [LICENSE](#license)

## Installation
Install via [pip](https://pypi.org/project/django-clite/):
```bash
pip install django-clite
```

Install from source:
```
git clone https://github.com/oleoneto/django-clite.git
cd django-clite
pip install .
```

After installation, the CLI will expose the binary with the name:
```
django-clite
```

### Extending the CLI
If you would like to extend the functionality of this CLI, you can include your own `plugins/commands` by
setting an environment variable: `DJANGO_CLITE_PLUGINS`. Simply set this variable to the path where your plugins are.

## Dependencies
Check out [setup.py](setup.py) for all installation dependencies.

## Interactive Docs
In order to maintain consistency in our documentation of all the different commands and features of the CLI,
 we've decided to move the [README](docs/cli/readme.ipynb) to a series of Jupyter notebooks which you can explore per command under the [docs](docs) directory.

## To Do
[Check out our open issues](https://github.com/oleoneto/django-clite/issues).

## Pull requests
Found a bug? See a typo? Have an idea for new command?
Feel free to submit a pull request with your contributions. They are much welcome and appreciated.

## LICENSE
**django-clite** is [BSD Licensed](LICENSE.txt).
