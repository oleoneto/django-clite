import click

from geny.core.filesystem.files import File
from django_clite.decorators.scope import scoped, Scope


@scoped(to=Scope.PROJECT)
@click.command()
@click.option("--compose", is_flag=True)
@click.pass_context
def dockerfile(ctx, compose):
    """
    Generate a Dockerfile.
    """

    files = [
        File(name="Dockerfile", template="docker/dockerfile.tpl", context={}),
    ]

    if compose:
        files.append(
            File(
                name="docker-compose.yaml",
                template="docker/docker-compose.tpl",
                context={
                    "services": [
                        "database",
                        "redis",
                        "celery",
                    ],
                },
            )
        )

    [
        file.create(
            **ctx.obj,
        )
        for file in files
    ]
