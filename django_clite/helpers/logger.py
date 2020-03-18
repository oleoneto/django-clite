import click

DEFAULT_IMPORT_WARNING = "Module already imported. Skipping..."

DEFAULT_OVERRIDE_WARNING = "File {} already exists. Override file?"

DEFAULT_NOUN_NUMBER_WARNING = "Tip: resource name should be singular."

DEFAULT_NOUN_NUMBER_OPTION = "Change resource name from {} to {}?"

DEFAULT_PARSED_CONTENT_LOG = """Filename: {}\nFilepath: {}\n\n---- Begin content ----\n{}\n---- End content ----\n\n"""

DEFAULT_DESTROY_LOG = """Will delete...\nFilename: {}\nFilepath: {}\n\nWill also remove imports in __init__.py"""

DEFAULT_APP_CREATION_LOG = """Successfully created application: {}"""

DEFAULT_ERRORS = {
    "project": "Unable to create project. Will exit.",
    "app": "Unable to create app: {}. Skipping...",
    "package": "Unable to create package. Will exit.",
    "folder": "Unable to create folder. Skipping...",
    "repo": "Unable to initialize repository. Skipping...",
    "touch": "Unable to create default files. Skipping...",
    "clean": "Unable to remove default files. Skipping...",
}

DEFAULT_MANAGEMENT_ERROR = """The CLI could not decipher your django project.
Please try to create your app inside a Django project directory."""

DEFAULT_MANAGEMENT_ERROR_HELP = """If your project uses custom configuration, you can pass some context to the CLI:
    Specify the manage.py directory with the flag: --directory/-d
    Specify the project name with the flag: --project/-p
    
    Example:
    D create app classroom --project school --directory path/to/management
"""

DEFAULT_MANAGEMENT_TIP = """Tip:
If your project is called `website`, for example, 
you need to run `D create app app_name` from within `website` or `website/website`.
"""

DEFAULT_CREATE_MESSAGE = 'Successfully created {} for {}.'

DEFAULT_DELETE_MESSAGE = 'Successfully deleted {} for {}.'


def log_error(message, **kwargs):
    click.secho(message=message, **kwargs, fg='red')


def log_info(message, **kwargs):
    click.secho(message=message, **kwargs, fg='blue')


def log_success(message, **kwargs):
    click.secho(message=message, **kwargs, fg='green')


def log_standard(message, **kwargs):
    click.secho(message=message, **kwargs)


def log_verbose(header, message):
    if header:
        click.secho(f'{header}', bold=True)
    click.secho(f'{message}', bold=False)
