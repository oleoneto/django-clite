import os
from django_clite.helpers import FSHelper
from django_clite.helpers.logger import log_info, log_standard, log_verbose


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
                log_standard(f'{app}', bold=True)
                
                if show_paths:
                    log_standard(f'{path}\n')

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

    def get_models(self, show_paths=False, no_stdout=False):
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

            for root, dirs, files in os.walk(models_directory):
                dirs[:] = [d for d in dirs if d not in excluded_dirs]
                files[:] = [f for f in files if f not in excluded_files]

                if files:
                    log_standard(app, bold=True)

                    if show_paths:
                        if not no_stdout:
                            log_standard(f'  {path}', bold=True)

                    for f in sorted(files):
                        models.append({app: f})
                        if not no_stdout:
                            log_verbose(
                                header=None,
                                message='    {0:20}'.format(f),
                            )
                    log_standard('')

        return models

    def parse_model_attributes(self):
        pass
