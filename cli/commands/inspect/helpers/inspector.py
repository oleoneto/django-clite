import os
import fileinput
from cli.helpers import FSHelper
from cli.helpers.logger import log_info, log_standard, log_verbose
import re


class InspectorHelper(FSHelper):

    def __init__(self, cwd, dry=False, force=False, default=False, verbose=False):
        super(InspectorHelper, self).__init__(cwd=cwd, dry=dry, force=force, default=default, verbose=verbose)

    def get_apps(self, show_paths=False, suppress_output=False):
        """
        Traverse file system in search for AppConfig files.

        :param show_paths: Toggle showing the path to each app
        :param suppress_output: Toggle printing to stdout
        :return: dictionary of app names and paths
        """

        current_apps = {
            c.rsplit('/', 1)[-1]: c
            for c, _, files in os.walk(self.cwd) if 'apps.py' in files
        }

        for app, path in sorted(current_apps.items()):

            if not suppress_output:
                log_standard(f'{app}', bold=True)

                if show_paths:
                    log_standard(f'{path}\n')

        return sorted(current_apps)

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

        [log_verbose(header=path, message=None) for path in current_paths]

        return current_paths

    def get_classes(self, scope, show_paths=False, suppress_output=False):
        """
        Retrieve models under each app's models package.

        :return:
        """

        models = []

        excluded_dirs = [
            '__pycache__',
            'abstract',
            'abstracts',
            'helpers',
            'inlines',
            'managers',
            'mixins',
            'permissions',
            'signals',
            'tests',
            'validators',
        ]

        excluded_files = [
            '__init__.py',
            'requires.py'
            'router.py',
        ]

        current_apps = {
            c.rsplit('/', 1)[-1]: c
            for c, _, files in os.walk(self.cwd) if 'apps.py' in files
        }

        # One day... one day I'll refactor this
        for app, path in sorted(current_apps.items()):

            if scope == 'managers':
                scope = 'models/managers'

            resource_directory = f'{path}/{scope}'

            for root, dirs, files in os.walk(resource_directory):
                dirs[:] = [d for d in dirs if d not in excluded_dirs]
                files[:] = [f for f in files if f not in excluded_files]

                if files and not suppress_output:
                    log_standard('')
                    log_standard(app, bold=True)

                    if show_paths:
                        if not suppress_output:
                            log_standard(f'  {resource_directory}', bold=True)

                for file in sorted(files):
                    models.append({app: file})
                    model_file = resource_directory + f'/{file}'

                    for line in fileinput.input(model_file):
                        if re.match(r'^class ', line):  # in line and "Meta:" not in line:
                            model_name = line.split('class ')[-1].split('(')[0]
                            if not suppress_output:
                                log_verbose(
                                    header=None,
                                    message='    {0:20}'.format(model_name),
                                )
                    fileinput.close()
        return models
