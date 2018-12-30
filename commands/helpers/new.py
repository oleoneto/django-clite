import os
import subprocess
import click
from commands.helpers.echoer import successful, error


class Helper:
    def show_files(self):
        # TODO: Implement show_files()
        # List all files in the current directory
        pass

    def create_project(self, current_dir, project_name):
        # TODO: Implement create_project()
        # Determine if a django project exists in the current directory
        # If so, prompt user to decide whether they want to proceed. Use `click.prompt()`

        pass

    def create_app(self, current_dir, app_name):
        # TODO: Implement create_app()
        # Get current directory from args
        # Check if `manage.py` exists in ../current_app_dir/
        pass

    def create_templates(self, current_app_dir):
        # TODO: Implement create_templates()
        #
        pass
