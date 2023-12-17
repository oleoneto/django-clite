import click

from cli.core.filesystem.files import File
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.PROJECT)
@click.command()
@click.option("--docker-compose", is_flag=True)
@click.pass_context
def dockerfile(ctx, docker_compose):
"""
Generate a Dockerfile.
"""

files = [
File(name=f"Dockerfile", template="docker/dockerfile.tpl", context={}),
]

if docker_compose:
files.append(
File(
name=f"docker-compose.yaml",
template="docker/docker-compose.tpl",
context={
"services": [],
},
)
)

[file.create(**ctx.obj,) for file in files]
