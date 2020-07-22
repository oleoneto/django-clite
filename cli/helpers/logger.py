import click as c

DEFAULT_IMPORT_WARNING = "Module already imported. Skipping..."

DEFAULT_OVERRIDE_WARNING = "File {} already exists. Override file?"

DEFAULT_NOUN_NUMBER_WARNING = "Tip: resource name should be singular."

DEFAULT_NOUN_NUMBER_OPTION = "Change resource name from {} to {}?"

DEFAULT_PARSED_CONTENT_LOG = """Filename: {}\nFilepath: {}\n\n---- Begin content ----\n{}\n---- End content ----\n\n"""

DEFAULT_DESTROY_LOG = """Will delete...\nFilename: {}\nFilepath: {}\n\nWill also remove imports in __init__.py"""

DEFAULT_APP_CREATION_LOG = """Successfully created application: {}"""

DEFAULT_MANAGEMENT_ERROR = """The CLI could not decipher your django project.
Please try to create your app inside a Django project directory."""

DEFAULT_DIRECTORY_ERROR = """The CLI could not decipher your django project."""

DEFAULT_MANAGEMENT_APP_ERROR_PROMPT = """The CLI could not find your django project. Proceed anyways?"""

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
    c.secho(message=message, **kwargs, fg='red')


def log_info(message, **kwargs):
    c.secho(message=message, **kwargs, fg='blue')


def log_success(message, **kwargs):
    c.secho(message=message, **kwargs, fg='green')


def log_standard(message, **kwargs):
    c.secho(message=message, **kwargs)


def log_verbose(header, message=None, **kwargs):
    if header:
        c.secho(message=f'{header}', bold=True, fg='blue', **kwargs)
    if message:
        c.secho(message=f'{message}', bold=False, **kwargs)
