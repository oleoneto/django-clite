"""
Django CLI

Requirements:
Python3.6, PIP, Django 2.1, and Git

Description:
A CLI that handles creating and managing Django projects
"""

import os, sys, shutil, click
from helpers.Logger import Logger

CURR_DIR = os.getcwd()
BASE_DIR = os.curdir
logger = Logger()


@click.group()
@click.pass_context
def main(ctx):
    """
    Django CLI
    """


@click.group()
@click.pass_context
def generate():
    pass


@generate.command()
def model():
    pass


@generate.command()
def route():
    pass


@generate.command()
def viewset():
    pass



















# @main.command()
# @click.option('--dump', help="Output history of commands to a file")
# def history(dump):
#     """
#     History of commands run through the CLI
#     """
#
#
# @main.command()
# @click.option('--dry-run', is_flag=True, help="Show output but DO NOT run.")
# @click.argument('resource')
# def generate(resource, dry_run):
#     """
#     Generates a resource
#     """
#
#
# @main.command()
# @click.option('--resource', help="Resource to be destroyed")
# @click.option('--dry-run', is_flag=True, help="Show output but DO NOT run.")
# def destroy(resource, dry_run):
#     """
#     Destroys a resource
#     """
#     proceed = click.confirm("Are you sure you want to destroy the resource?", show_default=True, default=False)
#
#
# @main.command()
# @click.option('--dry-run', is_flag=True, help="Show output but DO NOT run.")
# def migrate(dry_run):
#     """
#     Makes and applies migrations to DB
#     """
#
#
# @main.command()
# def directory():
#     """
#     Prints the current working directory
#     """
#     click.secho(CURR_DIR, fg='green')


if __name__ == '__main__':
    main()


# Similar to `cat infile.ext outfile.ext`
# shutil.copy('LICENSE', 'Django')

# Similar to `cp -r origin destination`
# shutil.copytree('dummy', 'DJ')
