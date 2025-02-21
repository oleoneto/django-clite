import click

from geny.core.filesystem.files import File
from django_clite.decorators.scope import scoped, Scope


@scoped(to=Scope.PROJECT)
@click.command()
@click.option("--docker-compose", is_flag=True)
@click.pass_context
def dockerfile(ctx, docker_compose):
    """
    Destroy a Dockerfile (and docker-compose.yaml).
    """

    files = [
        File(name="Dockerfile"),
    ]

    if docker_compose:
        files.append(File(name="docker-compose.yaml"))

    [
        file.destroy(
            **ctx.obj,
        )
        for file in files
    ]
