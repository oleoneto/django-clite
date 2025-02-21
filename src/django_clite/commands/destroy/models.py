import click

from pathlib import Path
from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import RemoveLineFromFile
from django_clite.core.logger import logger
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--api", is_flag=True, help="Destroy only related api resources")
@click.option("--full", is_flag=True, help="Destroy all related resources")
@click.option("--admin", is_flag=True, help="Destroy admin model")
@click.option("--fixtures", is_flag=True, help="Destroy model fixture")
@click.option("--form", is_flag=True, help="Destroy model form")
@click.option("--serializers", is_flag=True, help="Destroy serializers")
@click.option("--templates", is_flag=True, help="Destroy templates")
@click.option("--tests", is_flag=True, help="Destroy tests")
@click.option("--views", is_flag=True, help="Destroy views")
@click.option("--viewsets", is_flag=True, help="Destroy viewsets")
@click.pass_context
def model(
    ctx,
    name,
    api,
    full,
    admin,
    fixtures,
    form,
    serializers,
    templates,
    tests,
    views,
    viewsets,
):
    """
    Destroy a model.
    """

    if api and full:
        logger.error("Flags --api and --full cannot be used simultaneously.")
        raise click.Abort()

    File(name=f"models/{name}.py").destroy(
        after_hooks=[
            RemoveLineFromFile(
                Path("models/__init__.py"), command_defaults.model(name)
            ),
        ],
        **ctx.obj,
    )

    def destroy_related_resources():
        if admin or api or full:
            from .admin import admin as cmd

            ctx.invoke(cmd, name=name)

        if fixtures or api or full:
            from .fixtures import fixture as cmd

            ctx.invoke(cmd, model=name)

        if form or full:
            from .forms import form as cmd

            ctx.invoke(cmd, name=name)

        if serializers or api or full:
            from .serializers import serializer as cmd

            ctx.invoke(cmd, name=name)

        if templates or api or full:
            from .template import template as cmd

            ctx.invoke(cmd, name=name, full=full)

        if tests or api or full:
            from .tests import test as cmd

            ctx.invoke(cmd, name=name, full=full)

        if views or full:
            from .views import view as cmd

            ctx.invoke(cmd, name=name, full=full)

        if viewsets or api or full:
            from .viewsets import viewset as cmd

            ctx.invoke(cmd, name=name)

    destroy_related_resources()


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def scaffold(ctx, name):
    """
    Delete all resources for a given model.
    """

    ctx.invoke(model, name=name, full=True)
