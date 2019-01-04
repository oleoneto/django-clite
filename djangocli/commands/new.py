import click
import shutil
import subprocess
import os
from commands.gitter import git
from commands.helpers.new import *
from commands.helpers.echoer import successful, error

helper = Helper()

@click.group()
@click.pass_context
def new(ctx):
    """
    Creates new apps and projects
    """
    pass


@new.command()
@click.option('--path', help="Specify the path wherein the app should live")
@click.argument('name')
def app(path, name):
    """
    Creates a new app
    """
    # TODO: Implement method
    # TODO: add serializer, urls, and viewset files.

    name = name.lower()
    try:
        helper.create_app(".", name)
    except FileExistsError:
        error("App already exists")


@new.command()
@click.argument('name')
def project(name):
    """
    Creates a new project
    """

    # TODO: Implement method
    # TODO: Check if app exists?
    # TODO: Initialize repo
    try:
        helper.create_project(".", name)
    except FileExistsError:
        error("Project already exists")


@new.command()
@click.argument('name')
def requirement(name):
    """
    Adds new requirement to project
    """
    # TODO: Implement method
    pass
