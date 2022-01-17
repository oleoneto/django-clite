from typing import NamedTuple


class ExecutionResult(NamedTuple):
    code: str
    description: str


class SearchResults(NamedTuple):
    matches: dict = dict()


class GenericHandler:
    def __init__(self, cwd='.', dry=False, force=False, verbose=False, debug=False):
        self.__context = {
            'cwd': cwd,
            'dry': dry,
            'force': force,
            'verbose': verbose,
            'debug': debug
        }

    @property
    def current_directory(self):
        return self.__context['cwd']

    @property
    def forceful(self):
        return self.__context['force']

    @property
    def dry(self):
        return self.__context['dry']

    @property
    def verbose(self):
        return self.__context['verbose']

    @property
    def debug(self):
        return self.__context['debug']

    @property
    def errors(self):
        return {
            'error': ExecutionResult('error', description='An handled error occurred'),
            'file_exists': ExecutionResult('not_created', description='File was not created. File already exists.'),
            'file_does_not_exist': ExecutionResult('not_deleted', description='File was not deleted. File does not exist.'),
            "project": "Unable to create project. Will exit.",
            "app": "Unable to create app: {}. Skipping...",
            "package": "Unable to create package. Will exit.",
            "folder": "Unable to create folder. Skipping...",
            "repo": "Unable to initialize repository. Skipping...",
            "touch": "Unable to create default files. Skipping...",
            "clean": "Unable to remove default files. Skipping...",
            "creation_error": "An error occurred while attempting to create the project",
            "template_not_found": "Attempting to load a missing template caused an error.",
            "directory_not_found": "The CLI could not decipher your django project.",
            "management_not_found": """The CLI could not decipher your django project.\
            Please try to create your app inside a Django project directory.""",
        }

    @property
    def messages(self):
        return {
            "created": ExecutionResult('created', 'File was created successfully.'),
            "create_skipped": ExecutionResult('create_skipped', 'File was not created. Skipped with DRY flag.'),
            "not_created": ExecutionResult('not_created', 'File was not created.'),
            "deleted": ExecutionResult('deleted', 'File was deleted successfully.'),
            "delete_skipped": ExecutionResult('delete_skipped', 'File was not deleted. Skipped with DRY flag.'),
            "not_deleted": ExecutionResult('not_deleted', 'File was not deleted.'),
            "appended": ExecutionResult('appended', 'Content was appended successfully.'),
            "append_skipped": ExecutionResult('append_skipped', 'Content was not appended. Skipped with DRY flag.'),
            "not_appended": ExecutionResult('not_appended', 'Content was not appended.'),
            "un_appended": ExecutionResult('un_appended', 'Content was removed from file.'),
            "skipped_un_appended": ExecutionResult('skipped_un_appended', 'Content was not removed from file. Skipped with DRY flag.'),
            "directory_not_found_help": """If your project uses custom configuration, you can pass\
            some context to the CLI:\nSpecify the manage.py directory with the flag: --directory/-d\
            Specify the project name with the flag: --project/-p/
        
            Example:\
            D create app classroom --project school --directory path/to/management"""
        }
