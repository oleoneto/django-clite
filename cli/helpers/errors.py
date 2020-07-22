DEFAULT_ERRORS = {
    "project": "Unable to create project. Will exit.",
    "app": "Unable to create app: {}. Skipping...",
    "package": "Unable to create package. Will exit.",
    "folder": "Unable to create folder. Skipping...",
    "repo": "Unable to initialize repository. Skipping...",
    "touch": "Unable to create default files. Skipping...",
    "clean": "Unable to remove default files. Skipping...",
}

PROJECT_CREATION_ERROR = 'An error occurred while attempting to create the project'

PROJECT_DIRECTORY_NOT_FOUND_ERROR = """The CLI could not decipher your django project."""

PROJECT_MANAGEMENT_NOT_FOUND_ERROR = """The CLI could not decipher your django project.
Please try to create your app inside a Django project directory."""
