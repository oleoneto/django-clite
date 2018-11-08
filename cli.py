"""
Django CLI

Requirements:
Python3.6, PIP, Django 2.1, and Git

Description:
A CLI that handles creating and managing Django projects
"""

import os
import click
from commands.generator import generate
from commands.destroyer import destroy
from commands.migrator import db
from commands.new import new
from commands.installer import install


CURR_DIR = os.getcwd()
BASE_DIR = os.curdir


@click.group()
@click.pass_context
def main(ctx):
    """
    Django CLI v1
    """


main.add_command(generate)
main.add_command(destroy)
main.add_command(db)
main.add_command(new)
main.add_command(install)


if __name__ == '__main__':
    main()
