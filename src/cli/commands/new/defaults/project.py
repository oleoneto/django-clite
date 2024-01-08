# cli:commands:new:defaults:project
from cli.core.filesystem.files import File
from cli.core.filesystem.directories import Directory
from cli.core.filesystem.transformations import MoveFile

project_transformations = []


def new_project(name: str, **options) -> Directory:
    project_transformations.append(
        MoveFile("settings.py", "settings/__init__.py"),
    )

    proj = Directory(
        name=name,
        children=[
            Directory(
                name="settings",
                children=[
                    File(name="api.py", template="project/api.tpl"),
                    File(name="storage.py", template="project/storage.tpl"),
                ],
            ),
            File(name="constants.py", content="# your constants go here"),
        ],
    )

    root = Directory(
        name=name,
        children=[
            proj,
            Directory(name="staticfiles"),
            Directory(
                name="templates",
                children=[
                    File(name="404.html", template="app/404.tpl"),
                    File(name="500.html", template="app/500.tpl"),
                ],
            ),
            File(name=".env", template="project/env.tpl"),
            File(name=".gitignore", template="project/gitignore.tpl"),
            File(name="README.md", template="project/README.tpl"),
            File(name="requirements.txt", template="project/requirements.tpl"),
        ],
    )

    # Handle user options

    if options.get("github", False):
        root.add_children(
            [
                Directory(
                    ".github",
                    children=[
                        File(name="ci.yml", template="github/ci.tpl"),
                        File(
                            name="pull_request_template.md",
                            template="github/pull_request_template.tpl",
                        ),
                    ],
                )
            ]
        )

    if options.get("docker", False):
        root.add_children(
            [
                File(name=".dockerignore", template="docker/dockerignore.tpl"),
                File(name="Dockerfile", template="docker/dockerfile.tpl"),
                File(name="docker-compose.yml", template="docker/docker-compose.tpl"),
                File(
                    name="docker-entrypoint.sh", template="docker/docker-entrypoint.tpl"
                ),
            ]
        )

    if options.get("kubernetes", False):
        root.add_children(
            [
                Directory(
                    ".kubernetes",
                    children=[
                        File(
                            name="deployment.yaml", template="kubernetes/deployment.tpl"
                        ),
                        File(name="service.yaml", template="kubernetes/service.tpl"),
                        File(name="ingress.yaml", template="kubernetes/ingress.tpl"),
                        File(
                            name="configmap.yaml", template="kubernetes/configmap.tpl"
                        ),
                    ],
                ),
            ]
        )

    # TODO: implement celery option
    # if options.get("celery", False):

    # TODO: implement drf option
    # if options.get("drf", False):

    # TODO: implement dokku option
    # if options.get("dokku", False):

    # TODO: implement heroku option
    # if options.get("heroku", False):

    return root
