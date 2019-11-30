import os
from django_clite.helpers import FSHelper
from django_clite.helpers.logger import log_info, log_standard


class InspectorHelper(FSHelper):

    def get_apps(self, show_paths=False, no_stdout=False):
        """
        Traverse file system in search for AppConfig files.

        :param show_paths: Toggle showing the path to each app
        :param no_stdout: Toggle printing to stdout
        :return: dictionary of app names and paths
        """

        current_apps = {
            c.rsplit('/', 1)[-1]: c
            for c, _, files in os.walk(self.cwd) if 'apps.py' in files
        }

        for app, path in sorted(current_apps.items()):

            if not no_stdout:
                log_info(app)

            if show_paths:
                if not no_stdout:
                    log_standard(f"{path}")

        return current_apps

    def get_app_paths(self):
        """
        Traverse file system in search for apps and their paths.

        :return: list of app paths
        """

        current_paths = sorted([
            c
            for c, _, files in os.walk(self.cwd)
            if 'apps.py' in files
        ])

        [log_info(path) for path in current_paths]

        return current_paths

    def get_models(self):
        """
        Retrieve models under each app's models package.

        :return:
        """

        models = []

        excluded_dirs = [
            'signals', 'tests', 'helpers',
            'validators', 'managers', '__pycache__'
        ]

        excluded_files = [
            "__init__.py"
        ]

        current_apps = {
            c.rsplit('/', 1)[-1]: c
            for c, _, files in os.walk(self.cwd) if 'apps.py' in files
        }

        for app, path in sorted(current_apps.items()):

            models_directory = path + "/models"

            log_info(app)

            for root, dirs, files in os.walk(models_directory):
                dirs[:] = [d for d in dirs if d not in excluded_dirs]
                files[:] = [f for f in files if f not in excluded_files]

                for f in files:
                    models.append({app: f})
                    log_standard(f)

            log_standard("---")

        return models

    def parse_model_attributes(self):
        pass
