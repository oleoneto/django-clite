# django_clite:commands:new:defaults:project
from geny.core.filesystem.files import File
from geny.core.filesystem.directories import Directory
from geny.core.filesystem.transformations import MoveFile

project_transformations = []


def new_project(name: str, **context) -> Directory:
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

    if context.get("github", False):
        github = Directory(
            ".github",
            children=[
                Directory(
                    ".github",
                    children=[
                        File(name="ci.yml", template="github/ci.tpl"),
                        File(name="pull_request_template.md", template="github/pull_request_template.tpl"),
                    ],
                )
            ],
        )

        root.add_children(github) # noqa

    if context.get("docker", False):
        docker = [
            File(name=".dockerignore", template="docker/dockerignore.tpl"),
            File(name="Dockerfile", template="docker/dockerfile.tpl"),
            File(name="docker-compose.yml", template="docker/docker-compose.tpl"),
            File(name="docker-entrypoint.sh", template="docker/docker-entrypoint.tpl"),
        ]

        root.add_children(docker) # noqa

    if context.get("kubernetes", False):
        kubernetes = [
            Directory(
                ".kubernetes",
                children=[
                    File(name="deployment.yaml", template="kubernetes/deployment.tpl"),
                    File(name="service.yaml", template="kubernetes/service.tpl"),
                    File(name="ingress.yaml", template="kubernetes/ingress.tpl"),
                    File(name="configmap.yaml", template="kubernetes/configmap.tpl"),
                ],
            ),
        ]

        root.add_children(kubernetes) # noqa

    # TODO: implement celery option
    # if options.get("celery", False):

    # TODO: implement drf option
    # if options.get("drf", False):

    # TODO: implement dokku option
    # if options.get("dokku", False):

    # TODO: implement heroku option
    # if options.get("heroku", False):

    return root
