import click


def successful(message):
    click.secho(message, fg='green')


def error(message):
    click.secho(message, fg='red')


def file_created(filename=''):
    successful("Successfully created %s" % filename)


def file_exists(filename=''):
    error("File already exists %s" % filename)
