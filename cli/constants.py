# cli
from cli.core.filesystem import NullFS

FILE_SYSTEM_HANDLER = NullFS

# CLI configuration

CLI_NAME_KEY = "django-clite"
DJANGO_FILES_KEY = "django:files"
ENABLE_DEBUG_KEY = "enable:debug"
ENABLE_DRY_RUN_KEY = "enable:dry"
ENABLE_FORCE_KEY = "enable:force"
ENABLE_VERBOSITY_KEY = "enable:verbosity"
FILE_SYSTEM_HANDLER_KEY = "fshandler"

# Project information

APPLICATION_NAME_KEY = "app_name"
PROJECT_NAME_KEY = "project_name"
