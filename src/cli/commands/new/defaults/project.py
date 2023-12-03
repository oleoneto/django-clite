# cli:commands:new:defaults:project
from cli.core.filesystem import File, Directory


def new_project(name: str) -> Directory:
    proj = Directory(
        name=name,
        children=[
            Directory(
                name="settings",
                children=[
                    File(name="api.py", template="project/api.tpl"),
                    File(name="database.py", template="project/database.tpl"),
                    File(name="settings.py", template="project/settings.tpl"),
                    File(name="storage.py", template="project/storage.tpl"),
                ],
            ),
            File(name="__init__.py", template="shared/init.tpl"),
            File(name="urls.py", template="project/urls.tpl"),
            File(name="asgi.py", template="project/asgi.tpl"),
            File(name="wsgi.py", template="project/wsgi.tpl"),
            File(name="constants.py", template="project/empty.tpl"),
        ],
    )

    root = Directory(
        name=name,
        children=[
            proj,
            Directory(
                ".github",
                children=[
                    File(name="ci.yml", template="github/ci.tpl"),
                    File(
                        name="pull_request_template.md",
                        template="github/pull_request_template.tpl",
                    ),
                ],
            ),
            Directory(name="staticfiles"),
            Directory(
                name="templates",
                children=[
                    File(name="404.html", template="app/404.tpl"),
                    File(name="500.html", template="app/500.tpl"),
                ],
            ),
            File(name="manage.py", template="project/manage.tpl"),
            File(name=".env", template="project/env.tpl"),
            File(name=".env-example", template="project/env.tpl"),
            File(name=".gitignore", template="project/gitignore.tpl"),
            File(name=".dockerignore", template="docker/dockerignore.tpl"),
            File(name="Dockerfile", template="docker/dockerfile.tpl"),
            File(name="docker-compose.yml", template="docker/docker-compose.tpl"),
            File(name="docker-entrypoint.sh", template="docker/docker-entrypoint.tpl"),
            File(name="README.md", template="project/README.tpl"),
            File(name="requirements.txt", template="project/requirements.tpl"),
        ]
    )

    return root
