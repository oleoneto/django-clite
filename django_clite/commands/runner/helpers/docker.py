import os
from django_clite.helpers.logger import *
from django_clite.helpers import rendered_file_template
from .runner import RunnerHelper

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('tpl')]


class DockerHelper(RunnerHelper):

    def run(self, **kwargs):
        pass

    def create_compose(self, project, **kwargs):

        template = 'docker-compose.tpl'
        filename = 'docker-compose.yml'

        try:
            os.chdir(project)

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

    def create_dockerfile(self, project):

        template = 'dockerfile.tpl'
        filename = 'Dockerfile'

        try:
            os.chdir(project)

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
