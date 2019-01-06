import click
import os


def log_success(message):
    click.secho(message, fg='green')


def log_error(message):
    click.secho(message, fg='red')


def file_created(filename=''):
    log_success("Successfully created %s" % filename)


def file_exists(filename=''):
    log_error("File already exists %s" % filename)


