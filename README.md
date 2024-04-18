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

After installation, the CLI will expose the binary with the name:
```
django-clite
```

## Extending the CLI

Currently, there are two main ways of extending the functionality of the CLI:
1. Adding your own commands/plugins
2. Overriding the provided resource templates

### Including your own commands

If you would like to extend the functionality of this CLI, you can include your own `plugins/commands` by
setting an environment variable: `DJANGO_CLITE_PLUGINS`. Simply set this variable to the path where your plugins are.

Plugin commands are auto-discovered if they are placed under the plugins directory,
but please be sure to do the following for this to work:
1. **Name your package and click command the same**. That is, a package called `get`, for example, should define a `get` command.
2. **Place the command definition within the package's `main.py` module**. For example:
```python
# get/main.py
import click


@click.command()
@click.pass_context
def get(ctx):
    pass
```
3. **Sub-commands should be added to the top-most command group in the package's `main.py` module.**
```python
# get/main.py
import click


@click.group() # <- group
@click.pass_context
def get(ctx):
  pass


@click.command()
@click.pass_context
def foo(ctx):
  pass


get.add_command(foo)
```
4. **Access your commands via your top-most command group.**
```
django-clite get foo
```

**NOTE:** If you would like to skip a plugin/command from being auto-discovered, simply rename the package by either
prepending or appending any number of underscores (`_`). Any code contained within the package will be ignored.

### Overriding the templates

The flag `--templates-dir` can be used to configure an additional path wherein the CLI can look for resource templates.
Alternatively, you can use the environment variable `DJANGO_CLITE_TEMPLATES_DIR` for the same purpose.

Take a look at the [template files directory](django_clite/cli/template_files) for a reference of what files can be overriden. The
paths of the templates you wish to override need to match the provided template. For example, if you wish to override the
model template, which is defined under [`src/cli/template_files/models/model.tpl`](django_clite/cli/template_files/models/model.tpl),
you should define your own model template under your desired directory, i.e `/path/to/templates/models/model.tpl`.

## Development

### Install from source:
```
git clone https://github.com/oleoneto/django-clite.git
cd django-clite
pip install --editable .
```

### Dependencies
Check out [pyproject.toml](pyproject.toml) for all installation dependencies.

## Interactive Docs
In order to maintain consistency in our documentation of all the different commands and features of the CLI,
 we've decided to move the [README](docs/cli/readme.ipynb) to a series of Jupyter notebooks which you can explore per command under the [docs](docs) directory.

## To Do
[Check out our open issues](https://github.com/oleoneto/django-clite/issues).

## Pull requests
Found a bug? See a typo? Have an idea for new command?
Feel free to submit a pull request with your contributions. They are much welcome and appreciated.

## LICENSE
**django-clite** is [BSD Licensed](LICENSE).
