import click
from cli.utils import sanitized_string_callback
from cli.core.filesystem.filesystem import File, FileSystem
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.PROJECT)
@click.command()
# @click.argument("name", default="Dockerfile", callback=sanitized_string_callback)
@click.option("--docker-compose", is_flag=True)
@click.pass_context
def dockerfile(ctx, docker_compose):
    """
    Generate a Dockerfile.
    """

    files = [
        File(
            path=f"Dockerfile",
            template="docker/dockerfile.tpl",
            context={},
        ),
    ]

    if docker_compose:
        files.append(
            File(
                path=f"docker-compose.yaml",
                template="docker/docker-compose.tpl",
                context={
                    "services": [],
                },
            )
        )

    for file in files:
        FileSystem().create_file(
            file=file,
            content=TemplateParser().parse_file(
                filepath=file.template,
                variables=file.context,
            ),
        )
