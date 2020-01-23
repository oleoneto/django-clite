import os
import subprocess
from django_clite.helpers.logger import *
from django_clite.helpers import rendered_file_template
from .runner import RunnerHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]

BUILD_COMMAND = ['docker-compose', 'build']

START_COMMAND = ['docker-compose', 'up']


class DockerHelper(RunnerHelper):

    def run(self, **kwargs):
        pass

    def __create(self, project, template, filename):

        try:
            os.chdir(self.cwd)

            content = rendered_file_template(
                path=TEMPLATE_DIR,
                template=template,
                context={'project': project}
            )
            self.create_file(
                content=content,
                filename=filename
            )
            log_success(f"Created {filename}")
        except FileNotFoundError:
            log_error(f"Unable to create {filename}")

    def create_compose(self, project):

            template = 'docker-compose.tpl'
            filename = 'docker-compose.yml'

            self.__create(project, template, filename)

    def create_dockerfile(self, project):

        template = 'dockerfile.tpl'
        filename = 'Dockerfile'

        self.__create(project, template, filename)
        self.__create(project, 'docker-entrypoint.tpl', 'docker-entrypoint.sh')

    def build(self, verbose=False):

        try:
            os.chdir(self.cwd)
        except FileNotFoundError:
            pass

        try:
            if verbose:
                BUILD_COMMAND.insert(1, '--verbose')
            return subprocess.check_output(BUILD_COMMAND)
        except subprocess.CalledProcessError as e:
            return None

    def start(self, verbose=False):

        try:
            os.chdir(self.cwd)
        except FileNotFoundError:
            pass

        try:
            if verbose:
                START_COMMAND.insert(1, '--verbose')
            return subprocess.check_output(START_COMMAND)
        except subprocess.CalledProcessError as e:
            return None
