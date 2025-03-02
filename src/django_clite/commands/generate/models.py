import click
import pathlib
import inflection

from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import AddLineToFile, TouchFile

from django_clite.core.logger import logger
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback, fields_callback
from django_clite.constants import APPLICATION_NAME_KEY


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.argument("fields", nargs=-1, required=False, callback=fields_callback)
@click.option("-a", "--abstract", is_flag=True, help="Creates an abstract model type")
@click.option("--api", is_flag=True, help="Adds only related api resources")
@click.option("--full", is_flag=True, help="Adds all related resources")
@click.option("--admin", is_flag=True, help="Register admin model")
@click.option("--fixtures", is_flag=True, help="Create model fixture")
@click.option("--form", is_flag=True, help="Create model form")
@click.option("--serializers", is_flag=True, help="Create serializers")
# @click.option("--templates", is_flag=True, help="Create templates")
@click.option("--tests", is_flag=True, help="Create tests")
@click.option("--views", is_flag=True, help="Create views")
@click.option("--viewsets", is_flag=True, help="Create viewsets")
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def model(
    ctx,
    name,
    fields,
    abstract,
    api,
    full,
    admin,
    fixtures,
    form,
    serializers,
    # templates,
    tests,
    views,
    viewsets,
    skip_import,
):
    """
    Generates a model under the models directory.
    One can specify multiple attributes after the model's name, like so:

        django-clite g model track int:number char:title fk:album bool:is_favorite

    This will generate a Track model and add a foreign key of Album.
    If the model is to be added to admin.site one can optionally opt in by specifying the --register-admin flag.
    """

    if api and full:
        logger.error("Flags --api and --full cannot be used simultaneously.")
        raise click.Abort()

    current_app_scope = ctx.obj.get(APPLICATION_NAME_KEY)

    file = File(
        name=f"models/{name}.py",
        template="models/model.tpl",
        context={
            "api": api,
            "abstract": abstract,
            "classname": inflection.camelize(name),
            "fields": fields,
            "imports": dict((k, v) for k, v in fields.items() if v.is_relationship),
            "name": name,
            "table_name": f"{current_app_scope}.{inflection.pluralize(name)}",
        },
    )

    after_hooks = [TouchFile("models/__init__.py")]

    if not skip_import:
        after_hooks.append(
            AddLineToFile(
                pathlib.Path("models/__init__.py"),
                command_defaults.model(name),
                prevent_duplicates=True,
            )
        )

    file.create(after_hooks=after_hooks, **ctx.obj)

    def generate_related_resources():
        if admin or api or full:
            from .admin import admin as cmd

            ctx.invoke(cmd, name=name, fields=fields, skip_import=skip_import)

        if fixtures or api or full:
            from .fixtures import fixture as cmd

            ctx.invoke(cmd, model=name, fields=fields)

        if form or full:
            from .forms import form as cmd

            ctx.invoke(cmd, name=name, skip_import=skip_import)

        if serializers or api or full:
            from .serializers import serializer as cmd

            ctx.invoke(cmd, name=name, skip_import=skip_import)

        if tests or api or full:
            from .tests import test as cmd

            ctx.invoke(cmd, name=name, full=full)

        if views or full:
            from .views import view as cmd

            ctx.invoke(cmd, name=name, full=full, skip_import=skip_import)

        if viewsets or api or full:
            from .viewsets import viewset as cmd

            ctx.invoke(cmd, name=name, skip_import=skip_import)

    generate_related_resources()


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.argument("fields", nargs=-1, required=False, callback=fields_callback)
@click.option("--api", is_flag=True, help="Destroy only related api resources")
@click.pass_context
def scaffold(ctx, name, fields, api):
    """
    Generate all resources for a given model.
    """

    ctx.invoke(model, name=name, fields=fields, full=not api, api=api)
